class Empty:
	def __getattr__(self, name):
		return "zzz"
	
trans = Empty()

#NOTE: Mechanic toolbox and member info screens have not been set up for translation.
#	This can be fixed when I get back from my tour. -AJ

#Mechanic password dialog prompt
trans.enterPassword = "Enter Mechanic Password"
trans.passwordLabel = "Password:"
#First part of the phrase that appears in the dialgog. {0} is one of the actions below
trans.mechanicPermission = "You need a mechanic's permission to {0}."
#Actions that need a mechanic to type a passoword
trans.authenticateGeneric = "do that" #Generic action
trans.authenticateView = "view info for {0}" #{0} is a name
trans.authenticateWindowClose = "close the signin program"
trans.authenticateWorktrade = "do worktrade"
trans.authenticateVolunteer = "volunteer"
trans.authenticateToolbox = "use the mechanic toolbox"

#Title of main window
trans.mainWindowTitle = u"Welcome To The Bike Church!"

#Field descriptions for patron values
trans.patronFirstName = "First Name"
trans.patronLastName = "Last Name"

#Field descriptions for member values
trans.memberStart = "Start Date"
trans.memberEnd = "End Date"
trans.memberDonation = "Donation $"
trans.memberPhone = "Phone Number"
trans.memberEmail = "Email Address"
trans.memberSnailmail = "Mail Address"
trans.memberNotes = "Notes"

#Descriptions of shoptime types
trans.shoptimeTypeWorking = "working on a bike"
trans.shoptimeTypeParts = "looking for parts"
trans.shoptimeTypeWorktrade = "doing worktrade"
trans.shoptimeTypeVolunteer = "volunteering"

#Field descriptions for shoptime values
trans.shoptimeStart = "Start"
trans.shoptimeEnd = "End"
trans.shoptimeType = "Type"
trans.shoptimeNotes = "Notes"

#Field descriptions for Bike values
trans.bikeType = "Type"
trans.bikeColor = "Color"
trans.bikeBrand = "Brand"
trans.bikeModel = "Model"
trans.bikeSerial = "Serial #"

#Field descriptions for Feedback
trans.feedbackName = "Your Name (Optional)"
trans.feedbackFeedback = "Your Feedback"

#Errors that flash if you have entered invalid/incomplete info in an editor dialog
trans.signinSelectTask = "Select a task."
trans.signinEnterName = "Type your name."
trans.sigininAlreadySignedIn = "{0} is already {1}." #{0} is a name, {1} is an activity
trans.editPersonFirstName = "You must enter at least your first name."
trans.editPersonThreeLetters = "Your name must have at least three letters."
trans.editPersonAlreadyExists = "There's already somebody with that name in the database."
trans.editBikeNotEnoughInfo = "You need at least the color, type, and serial # for your bike."
trans.editShoptimeNoFuture = "Shoptime may not start in the future."
trans.editShoptimeNoTimeTravel = "End time must be later than start time."
trans.editShoptimeNeedType = "You must select a type."
trans.editFeedbackNeedFeedback = "Please enter your feedback."

#Occupants button labels
trans.occupantViewButton = "View Info"
trans.occupantSignoutButton = u"Sign Out"
#Occupant list column headers
trans.occupantListHeader = u"Who's in the Shop:"
trans.occupantColumnName = u"Name"
trans.occupantColumnActivity = u"Activity"
trans.occupantColumnTime = u"Time In Shop"

#Signin panel info
trans.signinIntro = u"Sign In Here"
trans.signinGreeting = u"Hi! Type your name here:"
trans.signinClickName = u"Click your name in the\nlist if it's here:"

#Signin choice intro
trans.signinIntro = u"What do you want to do?"
#Signin panel shoptime button labels
trans.signinShoptime = u"Work on my bike!"
trans.signinParts = u"Look for parts!"
trans.signinWorktrade = u"Do work trade!"
trans.signinVolunteer = u"Volunteer!"

#Statusbar buttons
trans.statusButtonFeedback = u"Leave Feedback"
trans.statusButtonToolbox = u"Mechanic's Toolbox"

#Editor window title prefixes
trans.editEditTitle = "Edit {0}" #{0} is a type of thing being edited from list below
trans.editAddTitle = "Add {0}" #{0} is a type of thing being added from list below
#Editor window title suffixes
trans.editShoptime = "Shoptime"
trans.editBike = "Bike"

#Feedback window title
trans.feedbackTitle = "Leave Feedback"

#New person window
trans.newPersonTitle = "New Person Information"
trans.newPersonIntro = "Since you haven't used this system before, please tell us your name and bike information."
trans.newPersonNameTitle = u"Your Name"
trans.newPersonNameIntro = u"Type Your Name:"
trans.newPersonBikeTitle = u"Your Bike"
trans.newPersonBikeIntro = "Describe Your Bike (if you have one):"

#Uncommenting the folliwng line will display all translatable strings as "xxx" in the program
#trans = Empty()
