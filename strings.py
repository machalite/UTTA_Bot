class Strings:
    def __init__(self):
        # command keywords
        self.REGISTER = "!register"
        self.TODAY = "!today"
        self.CHECKROOM = "!checkroom"
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
        self.ERR_FATAL = "Exception error. Please contact administrator!"
        # URLs
        self.IMGUR_UTTA = "http://imgur.com/Hn0d1DJ"
        # long strings
        self.ABOUT = "UNIVERSITY TIME TABLE BOT\nCreated by Jonathan"
        # messages on !register
        self.REG_SUCCESS = "Sucessfully registered!"
        self.REG_ALREADY = "You are already registered"
        self.UNREG = "You are not registered. Please register using !register."
        self.REG_INVALID = "Invalid code! Please try again or contact administrator for more information."
        self.REG_EXPIRED = "Expired authentication code! Please contact administrator."
        self.REG_FAILED = "Registration failed! Please contact administrator for assistance"
        # messages on !today
        self.TODAY_EMPTY = "There is no class for today"
        self.TODAY_HEADER = "Today's schedule:\n"
        # messages on !checkroom
        self.ROOM_HEADER = "Today's schedule for "
        self.ROOM_UNREG = "Room not found. Please try again"
        self.ROOM_EMPTY = "There is no class in this room for today"
        # messages on !schedule
        self.SCHEDULE_HEADER = "Weekly schedule:\n"
        self.SCHEDULE_MON = "Monday:"
        self.SCHEDULE_TUE = "Tuesday:"
        self.SCHEDULE_WED = "Wednesday:"
        self.SCHEDULE_THU = "Thursday:"
        self.SCHEDULE_FRI = "Friday:"
        self.SCHEDULE_SAT = "Saturday:"
        self.SCHEDULE_SUN = "Sunday:"
        # messages on !next
        self.NEXT_HEADER = "Next class:\n"
        self.NEXT_NOCLASS = "No more class for today!"
        # console messages
        self.CONS_INPUT = "User input message:"
