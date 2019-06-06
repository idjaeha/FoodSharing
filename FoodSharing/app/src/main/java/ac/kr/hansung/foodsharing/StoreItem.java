package ac.kr.hansung.foodsharing;

public class StoreItem {

    String storeName;
    String storeCategory;
    int restNum, x, y;

    public StoreItem(String name) {
        storeName = name;
        restNum = -1;
    }

    public StoreItem(String name, String categoryName, int restNum, int x, int y) {
        storeName = name;
        this.storeCategory = categoryName;
        this.restNum = restNum;
        this.x = x;
        this.y = y;
    }

    public String getStoreName() {
        return storeName;
    }

    public void setStoreName(String storeName) {
        this.storeName = storeName;
    }

    public String getStoreCategory() {
        return storeCategory;
    }

    public void setStoreCategory(String categoryName) {
        this.storeCategory = categoryName;
    }

    public int getRestNum() {
        return restNum;
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

    public void setRestNum(int restNum) {
        this.restNum = restNum;
    }
}
