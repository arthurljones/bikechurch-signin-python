import mimetypes, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from email.encoders import encode_base64

def DoEmail():
	sendMail("thebikechurch@gmail.com", "xxx", #real password goes here... todo
		"arthur.l.jones@gmail.com", "test", "testing")

def _GetAttachment(attachmentFilePath):
	contentType, encoding = mimetypes.guess_type(attachmentFilePath)

	if contentType is None or encoding is not None:
		contentType = 'application/octet-stream'

	mainType, subType = contentType.split('/', 1)
	file = open(attachmentFilePath, 'rb')

	if mainType == 'text':
		attachment = MIMEText(file.read())
	elif mainType == 'message':
		attachment = email.message_from_file(file)
	elif mainType == 'image':
		attachment = MIMEImage(file.read(), _subType = subType)
	elif mainType == 'audio':
		attachment = MIMEAudio(file.read(), _subType = subType)
	else:
		attachment = MIMEBase(mainType, subType)
		
	attachment.set_payload(file.read())
	encode_base64(attachment)

	file.close()

	attachment.add_header('Content-Disposition', 'attachment',
		filename = os.path.basename(attachmentFilePath))
	return attachment

def SendMail(user, password, recipient, subject, text, *attachmentFilePaths):
	msg = MIMEMultipart()
	msg['From'] = user
	msg['To'] = recipient
	msg['Subject'] = subject
	msg.attach(MIMEText(text))

	for attachmentFilePath in attachmentFilePaths:
		msg.attach(_GetAttachment(attachmentFilePath))

	mailServer = smtplib.SMTP('smtp.gmail.com', 587)
	mailServer.ehlo()
	mailServer.starttls()
	mailServer.ehlo()
	mailServer.login(user, password)
	mailServer.sendmail(user, recipient, msg.as_string())
	mailServer.close()

	print('Sent email to %s' % recipient)


