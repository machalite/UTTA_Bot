class Strings:
    def __init__(self):
        # command names
        self.REGISTER = "!register"
        self.TODAY = "!today"
        self.ROOMCHECK = "!roomcheck"
        self.SCHEDULE = "!schedule"
        self.NEXT = "!next"
        self.WHERE = "!where"
        self.CHECK = "!check"
        self.CHANGES = "!changes"
        self.TRANSLATE = "!translate"
        self.SEARCH = "!search"
        self.HELP = "!help"
        # instructions
        self.INST_REGISTER = "Register your student ID for personalised time table.\nExample !register 2013042032"
        # error messages
        self.ERR_PC = "This command is incompatible on LINE PC"
        self.ERR_FATAL = "Failed"
        # URLs
        self.IMGUR_UTTA = "http://imgur.com/Hn0d1DJ"
        # long strings
        self.ABOUT = "UNIVERSITY TIME TABLE BOT\nCreated by Jonathan"
        # messages on !register
        self.UNREG = "You are not registered. Please register using !register."
        self.REG_INVALID = "Invalid PIN! Please try again or contact administrator for more information."
        self.REG_EXPIRED = "PIN already used! Please try again or contact administrator for more information."
        self.REG_FAILED = "Registration failed! Please contact administrator for assistance"
        # messages on !today
        self.TODAY_EMPTY = "There is no class for today"
        # messages on !roomcheck
        self.ROOM_UNREG = "Room not found. Please try again"
        self.ROOM_EMPTY = "There is no class for in this room for today"
