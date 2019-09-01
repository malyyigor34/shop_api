class IpBlocked(Exception):
    def __init__(self, msg, *args, **kwargs):
        super(IpBlocked, self).__init__(*args, **kwargs)
        print(msg)