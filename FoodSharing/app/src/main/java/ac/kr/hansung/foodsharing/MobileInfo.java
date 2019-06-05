package ac.kr.hansung.foodsharing;

import java.util.ArrayList;

public class MobileInfo {
    String id, pwd;
    int userNum;
    int x, y;
    int foodNum;
    String[] top5Food;
    String nickName;
    boolean isConnectServer;
    boolean isSocketStart;
    ArrayList<String[]> messages;

    public String getNickName() {
        return nickName;
    }

    public void setNickName(String nickName) {
        this.nickName = nickName;
    }

    public boolean isConnectServer() {
        return isConnectServer;
    }

    public void setConnectServer(boolean connectServer) {
        isConnectServer = connectServer;
    }

    public boolean isSocketStart() {
        return isSocketStart;
    }

    public void setSocketStart(boolean socketStart) {
        isSocketStart = socketStart;
    }

    public String[] getTop5Food() {
        return top5Food;
    }

    public void setTop5Food(String[] top5Food) {
        this.top5Food = top5Food;
    }

    public MobileInfo(int userNum, String id, String pwd) {
        this.id = id;
        this.nickName = "hello world";
        this.pwd = pwd;
        this.userNum = userNum;
        this.x = this.y = 5;
        this.foodNum = -1;
        this.top5Food = new String[5];
        for (int i = 0; i < 5; i++) {
            this.top5Food[i] = "";
        }
        this.isConnectServer = false;
        this.isSocketStart = false;
        this.messages = new ArrayList<String[]>();
        messages.add(new String[]{"1", "jaeha", "hello"});

    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getPwd() {
        return pwd;
    }

    public void setPwd(String pwd) {
        this.pwd = pwd;
    }

    public int getUserNum() {
        return userNum;
    }

    public void setUserNum(int userNum) {
        this.userNum = userNum;
    }

    public int getX() {
        return x;
    }

    public void setX(int x) {
        this.x = x;
    }

    public int getY() {
        return y;
    }

    public void setY(int y) {
        this.y = y;
    }
}
