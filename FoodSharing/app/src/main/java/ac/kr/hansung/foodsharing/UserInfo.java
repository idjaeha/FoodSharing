package ac.kr.hansung.foodsharing;

public class UserInfo {
    String id, pwd;
    int userNum;
    int x, y;
    String[] foodNum;

    public UserInfo(int userNum, String id, String pwd) {
        this.id = id;
        this.pwd = pwd;
        this.userNum = userNum;
        this.x = this.y = 0;
        this.foodNum = new String[5];
        for (int i = 0; i < 5; i ++) {
            this.foodNum[i] = "";
        }
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

    public String[] getFoodNum() {
        return foodNum;
    }

    public void setFoodNum(String[] foodNum) {
        this.foodNum = foodNum;
    }
}
