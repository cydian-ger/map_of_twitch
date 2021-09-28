from viewer_handling.get_response import get_proxies, is_live, get_response
import os.path
from os import path

OK = "OK"

"""
REQUEST AND RESPONSE STATUS
"""


def proxies_up():
    NAME = "Proxy status: "
    try:
        length = len(get_proxies())
        if length > 0:
            return NAME + OK + " - %s proxies" % length
        else:
            return NAME + "Err -> %s proxies" % length
    except Exception as e:
        return NAME + repr(e)


def gql_up():
    NAME = "GQL status:   "
    try:
        is_live("renidrag_", None, throw_error=True)
        return NAME + OK
    except Exception as e:
        return NAME + repr(e)


def tmi_up():
    NAME = "TMI status:   "
    try:
        get_response("renidrag_", None, throw_error=True)
        return NAME + OK
    except Exception as e:
        return NAME + repr(e)


"""
File status
"""


def yaml_status() -> str:
    NAME = "YAML status:  "
    try:
        import settings
        return NAME + OK
    except Exception as e:
        return NAME + repr(e)


def dir_status() -> str:
    NAME = "DIR status:   "
    try:
        from settings import Viewer_Dir
    except Exception:
        return NAME + "YAML_Error"

    try:
        if path.exists(Viewer_Dir):
            print(Viewer_Dir)
            return NAME + OK
        else:
            raise NotADirectoryError("%s directory does not exist" % Viewer_Dir)
    except Exception as e:
        return NAME + repr(e)


def get_report() -> str:
    report_list = ["REQUEST STATUS", proxies_up(), gql_up(), tmi_up(),
                   "\nFILE STATUS", yaml_status(), dir_status(), ]
    return '\n'.join(report_list)


if __name__ == "__main__":
    print(get_report())
