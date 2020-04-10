from HID import Keyboard
import time
import re
import traceback

def execute_macro(text,execute=True, debug=False):
    log=[]

    if execute:
        try:
            kbd = Keyboard()
        except:
            log.append(dict(type="ERROR", line=0, message="Can't instantiate keyboard", long_message=traceback.format_exc()))
            return log

    for n,line in enumerate(text.split("\n")):
        line = line.strip()
        if len(line)==0:
            if debug:
                log.append(dict(type="DEBUG", line=n+1, message="Empty line"))
            continue
        if line[0]=='#':
            if debug:
                log.append(dict(type="DEBUG", line=n+1, message=f"Comment {line}"))
            continue

        m=re.match('"(.*)"',line)
        if m is not None:
            try:
                txt = line.encode('ascii').decode('unicode_escape')[1:-1]
                if debug:
                    log.append(dict(type="DEBUG", line=n+1, message=f"Write {repr(txt)}"))
                if execute:
                    kbd.write(txt)
            except:
                log.append(dict(type="ERROR", line=n+1, message="Write error", long_message=traceback.format_exc()))
                return log
            continue

        m=re.match('SLEEP ([0-9]*\.[0-9]+|[0-9]+)', line)
        if m is not None:
            try:
                t = float(m.group(1))
                if debug:
                    log.append(dict(type="DEBUG", line=n+1, message=f"Sleep {t}"))
                if execute:
                    time.sleep(t)
            except:
                log.append(dict(type="ERROR", line=n+1, message="Sleep error", long_message=traceback.format_exc()))
                return log
            continue
 
        try:
            if debug:
                log.append(dict(type="DEBUG", line=n+1, message=f"Press {line}"))
            if execute:
                kbd.press(line)
                kbd.release_all()
        except:
            log.append(dict(type="ERROR", line=n+1, message="Press error", long_message=traceback.format_exc()))
            return log
    log.append(dict(type="OK", line=n+1, message=f"Done"))

    return log
