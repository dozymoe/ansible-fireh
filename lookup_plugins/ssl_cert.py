from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase
import re

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()

BEGIN_PATTERN = re.compile(r'^-+BEGIN\s.*-+$')
END_PATTERN = re.compile(r'^-+END\s.*-+$')

class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):
        result = []

        for term in terms:
            display.debug(f"Extract ssl cert from cert file: {term}")

            lookup_file = self.find_file_in_search_path(variables, 'files',
                    term)
            display.vvvv(f"File lookup using {lookup_file} as file")
            try:
                if lookup_file:
                    contents, show_data = self._loader._get_file_contents(
                            lookup_file)

                    lines = [x for x in contents.decode('utf-8').splitlines()\
                            if x.strip()]
                    begin = None
                    end = None
                    for ii, line in enumerate(lines):
                        if BEGIN_PATTERN.match(line):
                            begin = ii
                        elif END_PATTERN.match(line):
                            end = ii
                    if begin is None or end is None:
                        raise AnsibleError(f"Cannot find cert string in {term}")

                    result.append('\n'.join(lines[begin:end+1]))
                else:
                    raise AnsibleParserError()
            except AnsibleParserError:
                raise AnsibleError(f"Could not locate file in lookup: {term}")

        return result
