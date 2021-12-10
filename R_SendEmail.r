install.packages('RDCOMClient', repos= 'http://www.omegahat.net/R')

library('RDCOMClient')
OutApp = COMCreate('Outlook.Application')

## Create an email
outMail= OutApp$CreateItem(0)

## Configure email parameter
outMail[['To']] = 'Tsepo.Moteuli@ashburton.co.za'
outMail[['subject']] = 'Test Email'
outMail[['body']] = 'Hi, How are you?'

## send it
outMail$Send()