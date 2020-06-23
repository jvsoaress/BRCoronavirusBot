from csv import DictReader, DictWriter


def check_user_in_database(userid):
    with open('users.csv', 'r') as arquivo:
        leitor = DictReader(f=arquivo)
        for linha in leitor:
            if linha['userid'] == str(userid):
                return True
        return False


def register(chatid, userid):
    try:
        if check_user_in_database(userid) is False:
            with open('users.csv', 'a') as arquivo:
                escritor = DictWriter(f=arquivo, fieldnames=['chatid', 'userid'])
                escritor.writerow({'chatid': chatid, 'userid': userid})
        else:
            return False
    except Exception as error:
        return error
    else:
        return True


# Returns a list of registered chat ids to send notification to
def notify():
    chatid_list = list()
    with open('users.csv', 'r') as arquivo:
        leitor = DictReader(f=arquivo)
        for linha in leitor:
            chatid_list.append(linha['chatid'])
    return chatid_list


if __name__ == '__main__':
    print(notify())
