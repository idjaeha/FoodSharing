# FoodSharing
Made by Hansung University



# branch 관련 명령어와 절차

## 명령어

git branch          : 모든 branch를 보여주고 현재 branch가 무엇인지 보여줌

git branch name     : name에 해당하는 branch를 생성함

git checkout name   : 현재 branch를 name에 해당하는 branch로 전환

git merge name      : 현재 branch와 name에 해당하는 branch를 자동으로 합침

git branch -d name  : name에 해당하는 branch를 삭제함



## 사용 절차

1. git branch name 을 이용하여 branch를 생성한다.
2. git checkout name 을 이용하여 임의의 branch를 생성한다.
3. 코드 작업을 한다.
4. 코드 작업을 마친 뒤 git checkout master 를 이용하여 master branch로 이동한다.
5. git merge name 을 이용하여 master와 합친다.
6. 무사히 합쳐졌다면 git add. -> git commit -m "message" -> git push를 이용하여 저장소에 올린다.
7. git branch -d name 을 이용하여 자신이 만든 branch를 지운다.
