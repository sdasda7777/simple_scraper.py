import requests, sys

requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
try:
    requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
except AttributeError:
    pass


SCRAPE_ONLY_UNPADDED: bool = False
NUMBER_BASE: int = 10
NUMBER_FORMAT_STRING: str = "{:d}"

# BASE_URL = "https://support.casio.com/storage/en/manual/pdf/EN/009/"
# NAME_PREFIX = "qw"
# NAME_SUFFIX = ".pdf"
# DIGITS_NO = 4


if __name__ == "__main__":
    if len(sys.argv) < 5 or len(sys.argv) > 6:
        print("Usage: " + sys.argv[0] + " BASE_URL NAME_PREFIX NAME_SUFFIX DIGITS_NO [START_NO=0]")
        print()
        print("Will scrape all files named NAME_PREFIXnumberNAME_SUFFIX from BASE_URL, where number is in [START_NO; NUMBER_BASE**DIGITS_NO-1]")
    else:
        BASE_URL = sys.argv[1]
        NAME_PREFIX = sys.argv[2]
        NAME_SUFFIX = sys.argv[3]
        DIGITS_NO = int(sys.argv[4])
        if len(sys.argv) == 6:
            START_NO = int(sys.argv[5])
        else:
            START_NO = 0
        
        for ii in range(START_NO, NUMBER_BASE**DIGITS_NO): # loops item numbers
            unpadded_string = NUMBER_FORMAT_STRING.format(ii)
            
            if SCRAPE_ONLY_UNPADDED:
                zero_pad_variations = range(len(unpadded_string), len(unpadded_string)+1)
            else:
                zero_pad_variations = range(len(unpadded_string), DIGITS_NO+1)
            
            for jj in zero_pad_variations:              # loops zero pad variations
                file_name = NAME_PREFIX + unpadded_string.zfill(jj) + NAME_SUFFIX
            
                response = requests.get(BASE_URL + file_name)

                print(str(response.status_code) + " on " + file_name)

                if response.status_code == 200:         # if OK, saves to file
                    with open(file_name,'wb') as local_file:
                        local_file.write(response.content)
