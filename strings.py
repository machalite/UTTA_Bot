class Strings:
    def __init__(self):
        # help content
        self.HELP_CONTENT = 'LIST OF COMMANDS\n\n'\
                            '!register <auth code>\nRegisters your LINE ID\n\n'\
                            '!today\nLists all classes for today\n\n'\
                            '!checkroom <room code or room name>\nLists all classes held in that room for today\n\n'\
                            '!schedule\nShows your weekly schedule\n\n'\
                            '!next\nShows information of next class\n\n'\
                            '!where\nShows requested room information\n\n'\
                            '!checkcourse\nShows requested course information\n\n'\
                            '!changes\nLists schedule changes'
        # command keywords
        self.REGISTER = "!register"
        self.TODAY = "!today"
        self.CHECKROOM = "!checkroom"
        self.SCHEDULE = "!schedule"
        self.NEXT = "!next"
        self.WHERE = "!where"
        self.CHECKCOURSE = "!checkcourse"
        self.CHANGES = "!changes"
        self.TRANSLATE = "!translate"
        self.SEARCH = "!search"
        self.HELP = "!help"
        self.ABOUT = "!about"
        # instructions
        self.INST_REGISTER = "Register your student ID for personalised time table.\nExample !register 2013042032"
        # error messages
        self.ERR_PC = "This command is incompatible on LINE PC"
        self.ERR_FATAL = "Exception error. Please contact administrator!"
        # URLs
        self.IMGUR_UTTA = "http://imgur.com/Hn0d1DJ"
        # long strings
        self.ABOUT_CONTENT = "UNIVERSITY TIME TABLE BOT\nCreated by Jonathan"
        # messages on !register
        self.REG_SUCCESS = "Registered successfully!"
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
        self.SCHEDULE_EMPTY = "You have not signed up for any classes"
        self.SCHEDULE_HEADER = "Weekly schedule:"
        self.SCHEDULE_MON = "Monday:"
        self.SCHEDULE_TUE = "Tuesday:"
        self.SCHEDULE_WED = "Wednesday:"
        self.SCHEDULE_THU = "Thursday:"
        self.SCHEDULE_FRI = "Friday:"
        self.SCHEDULE_SAT = "Saturday:"
        self.SCHEDULE_SUN = "Sunday:"
        # messages on !next
        self.NEXT_HEADER = "Next class:"
        self.NEXT_NOCLASS = "No more class for today!"
        # messages on !where
        self.WHERE_FLOOR = "Floor:"
        # messages on !checkcourse
        self.COURSE_INVALID = "Course not found. Please try again."
        self.COURSE_NOCLASS = "There is no class for this course yet."
        # messages on !changes
        self.CHANGES_HEADER = "Schedule changes:"
        self.CHANGES_CANCELLED = "Class cancelled"
        self.CHANGES_POSTPONED = "Class postponed to:"
        self.CHANGES_RELOCATED = "Class relocated to:"
        self.CHANGES_REPLACEMENT = "Replacement class"
        self.CHANGES_SUPPLEMENTARY = "Supplementary class"
        self.CHANGES_NOCHANGES = "No schedule changes"
        # console messages
        self.CONS_INPUT = "User input message:"
