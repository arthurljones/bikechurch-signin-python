#!/usr/bin/python
# -*- coding: utf-8 -*-

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
trans.mechanicPermission = "You need a mechanic's permission to {0}./Necesita el permiso de un@ mecanic@"
#Actions that need a mechanic to type a passoword
trans.authenticateGeneric = "do that" #Generic action
trans.authenticateView = "view info for {0}" #{0} is a name
trans.authenticateWindowClose = "close the signin program"
trans.authenticateWorktrade = "do worktrade/trabajar para credito"
trans.authenticateVolunteer = "volunteer/ser voluntario"
trans.authenticateToolbox = "use the mechanic toolbox"

#Title of main window
trans.mainWindowTitle = u"Welcome To The Bike Church!/Bienvenid@s a la Biciglesia!"

#Field descriptions for patron values
trans.patronFirstName = "First Name/Nombre"
trans.patronLastName = "Last Name/Apellido"

#Field descriptions for member values
trans.memberStart = "Start Date/Día de Inicio"
trans.memberEnd = "End Date/Día de Terminación"
trans.memberDonation = "Donation $/Donación"
trans.memberPhone = "Phone Number/Numero de teléfono"
trans.memberEmail = "Email Address/Dirección de correo electronico"
trans.memberSnailmail = "Mail Address/Dirección"
trans.memberNotes = "Notes/Notas"

#Descriptions of shoptime types
trans.shoptimeTypeWorking = "working on a bike/arreglando una bici"
trans.shoptimeTypeParts = "looking for parts/buscando partes"
trans.shoptimeTypeWorktrade = "doing worktrade/trabajando para credito"
trans.shoptimeTypeVolunteer = "volunteering/un voluntario"

#Field descriptions for shoptime values
trans.shoptimeStart = "Start/Inicio"
trans.shoptimeEnd = "End/Fin"
trans.shoptimeType = "Type/Tipo"
trans.shoptimeNotes = "Notes/Notas"

#Field descriptions for Bike values
trans.bikeType = "Type/Tipo"
trans.bikeColor = "Color"
trans.bikeBrand = "Brand/Marca"
trans.bikeModel = "Model/Modelo"
trans.bikeSerial = "Serial #/Numero de Serie"

#Field descriptions for Feedback
trans.feedbackName = "Your Name (Optional)/Su Nombre (si quiere)"
trans.feedbackFeedback = "Your Feedback/Su comentario"

#Errors that flash if you have entered invalid/incomplete info in an editor dialog
trans.signinSelectTask = "Select a task."
trans.signinEnterName = "Type your name./Escriba su nombre"
trans.sigininAlreadySignedIn = "{0} is already {1}." #{0} is a name, {1} is an activity
trans.editPersonFirstName = "You must enter at least your first name.\n/Necesita por lo menos escribir su nombre"
trans.editPersonThreeLetters = "Your name must have at least three letters."
trans.editPersonAlreadyExists = "There's already somebody with that name in the database."
trans.editBikeNotEnoughInfo = "You need at least the color, type, and serial # for your bike.\n/Necesita por lo menos el color, tipo, y el numero de serie de su bici."
trans.editShoptimeNoFuture = "Shoptime may not start in the future."
trans.editShoptimeNoTimeTravel = "End time must be later than start time."
trans.editShoptimeNeedType = "You must select a type."
trans.editFeedbackNeedFeedback = "Please enter your feedback."

#Occupants button labels
trans.occupantViewButton = "View Info"
trans.occupantSignoutButton = u"Sign Out"
#Occupant list column headers
trans.occupantListHeader = u"Who's in the Shop:\n/Quienes están en el Taller:"
trans.occupantColumnName = u"Name\n/Nombre"
trans.occupantColumnActivity = u"Activity\n/Actividad"
trans.occupantColumnTime = u"Time In Shop\n/Duración de Visita"

#Signin panel info
trans.signinIntro = u"Sign In Here/Firme aquí"
trans.signinGreeting = u"Hi! Type your name here:\n/Hola! Escriba su nombre aquí:"
trans.signinClickName = u"Click your name in the\nlist if it's here:/Sí aparece su \nnombre en la lista,\nhaz clic en el nombre:"

#Signin choice intro
trans.signinIntro = u"What do you \nwant to do?\n/Que es lo que \nquiere hacer?"
#Signin panel shoptime button labels
trans.signinShoptime = u"Work on my bike!\n/Arreglar mi bici"
trans.signinParts = u"Look for parts!\n/Buscar partes"
trans.signinWorktrade = u"Do work trade!\n/Trabajar para credito"
trans.signinVolunteer = u"Volunteer!\n/Voluntar"

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
trans.newPersonIntro = "Since you haven't used this system before, please tell us your name and bike information.\n/Como no ha usado el sistema antes, por favor entre su nombre y la información de la bici"
trans.newPersonNameTitle = u"Your Name/Su nombre"
trans.newPersonNameIntro = u"Type Your Name:/Entre su nombre:"
trans.newPersonBikeTitle = u"Your Bike/Su bici"
trans.newPersonBikeIntro = "Describe Your Bike (if you have one):\n/Describe su bici (si tiene una):"

#Uncommenting the folliwng line will display all translatable strings as "xxx" in the program
#trans = Empty()
