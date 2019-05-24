# FoodSharing
Made by Hansung University


# github 사용법

1. 인터넷에서 git을 다운받는다.
2. 윈도우 + r 를 눌러 실행창에 cmd를 입력 후 원하는 경로로 이동 후 본인이 원하는 기능을 사용한다.


github에서 처음 불러올때

- git clone https://github.com/idjaeha/FoodSharing.git


github에 저장

- git add .                              : 현재 디렉토리에 있는 모든 파일을 git에 저장

- git commit -m "20190329 액티비티 완성"  : 메모를 남긴다

- git push                               : 해당 파일에 맞는 github 저장소에 저장


github에서 불러오기

- git pull : github에 있는 자료를 로컬 저장소에 불러온다.



# branch 관련 명령어와 절차

명령어

- git branch          : 모든 branch를 보여주고 현재 branch가 무엇인지 보여줌

- git branch name     : name에 해당하는 branch를 생성함

- git checkout name   : 현재 branch를 name에 해당하는 branch로 전환

- git merge name      : 현재 branch와 name에 해당하는 branch를 자동으로 합침

- git branch -d name  : name에 해당하는 branch를 삭제함



사용 절차

1. git branch name 을 이용하여 branch를 생성한다.
2. git checkout name 을 이용하여 임의의 branch를 생성한다.
3. 코드 작업을 한다.
4. 코드 작업을 마친 뒤 git checkout master 를 이용하여 master branch로 이동한다.
5. git merge name 을 이용하여 master와 합친다.
6. 무사히 합쳐졌다면 git add. -> git commit -m "message" -> git push를 이용하여 저장소에 올린다.
7. git branch -d name 을 이용하여 자신이 만든 branch를 지운다.


