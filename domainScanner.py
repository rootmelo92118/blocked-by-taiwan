from typing import List

import logging
import dns.asyncresolver
import dns.message
import asyncio
import pathlib
import sys

logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

REDIRECT = {
    '165': '34.102.218.71',
    'TWNIC': '150.242.101.120',
    'unified_page': '182.173.0.181'
}


def split_list(list_input) -> List[List[str]]:
    output_list = []
    for i in range(0, len(list_input), 5):
        output_list.append(list_input[i:i + min(5, len(list_input) - i)])
    return output_list


class Checker:
    def __init__(self, raw: str, adguard: str, adguard_rewrote: str):
        self.raw_file = pathlib.Path(raw)
        self.adguard_file = pathlib.Path(adguard)
        self.rewrote_file = pathlib.Path(adguard_rewrote)
        self.tmp: str = ''
        if not self.raw_file.exists():
            self.raw_file.touch()
        if not self.adguard_file.exists():
            self.adguard_file.touch()
        if not self.rewrote_file.exists():
            self.rewrote_file.touch()

    def write(self, domain: str, ip: str):
        self.tmp = self.raw_file.read_text() + f'{domain}\n'
        self.raw_file.write_text(self.tmp)
        self.tmp = self.adguard_file.read_text() + f'||{domain}^\n'
        self.adguard_file.write_text(self.tmp)
        self.tmp = self.rewrote_file.read_text() + f'||{domain}^$dnsrewrite=NOERROR;A;{ip}\n'
        self.rewrote_file.write_text(self.tmp)
        self.tmp = ''


class Bun:
    def __init__(self, cht_ip: str = '168.95.1.1', raw: str = './raw.txt', adguard: str = './adguard.txt', adguard_rewrote: str = './reworte.txt'):
        self.cht_ip = cht_ip
        self.check = Checker(raw, adguard, adguard_rewrote)
        self.timedout: List[str] = []
        # self.bad: List[str] = []

    def get_filter_list(self, source: str = './source.txt') -> List[str]:
        with pathlib.Path(source) as file:
            if file.exists():
                return file.read_text().splitlines()
            else:
                raise Exception('Failed to open source file!')

    async def lookup(self, domain: str):
        q = dns.message.make_query(domain, 'A')
        try:
            r: dns.message.Message = await dns.asyncquery.udp(q, self.cht_ip, timeout=5)
        except dns.exception.Timeout:
            self.timedout.append(domain)
            logger.error(f'[Timeout] {domain}')
        except dns.query.BadResponse:
            # self.bad.append(domain)
            logger.error(f'[BadResponse] {domain}')
        else:
            if r.answer:
                ip = r.answer[0].to_text().split(' ')[-1]
                if ip in REDIRECT.values():
                    logger.info(f'[Redirect] {domain}')
                    self.check.write(f'{domain}', f'{ip}')
                else:
                    logger.error(f'[NotRedirect] {domain}')
            else:
                logger.error(f'[FailedResolve] {domain}')


async def main(source: str, raw: str = './raw.txt', adguard: str = './adguard.txt', adguard_rewrote: str = './reworte.txt'):
    bun = Bun(raw=raw, adguard=adguard, adguard_rewrote=adguard_rewrote)
    filterlist: List[List[str]] = split_list(bun.get_filter_list(source))
    # tasking = []

    for bunch in filterlist:
        tasking = [bun.lookup(e) for e in bunch]
        await asyncio.gather(*tasking)

    retries = 3
    while bun.timedout and retries > 0:
        logger.info(f'Retrying ... {retries}')
        retrylist: List[List[str]] = split_list(bun.timedout)
        bun.timedout = []
        for domain in retrylist:
            tasking = [bun.lookup(e) for e in domain]
            await asyncio.gather(*tasking)
        retries -= 1


if __name__ == '__main__':
    asyncio.run(main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4]))
