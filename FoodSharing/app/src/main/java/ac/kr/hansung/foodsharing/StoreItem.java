package ac.kr.hansung.foodsharing;

public class StoreItem {

    String storeName;
    String storeCategory;
    int restNum;

    public StoreItem(String name) {
        storeName = name;
        restNum = -1;
    }

    public StoreItem(String name, String categoryName, int restNum) {
        storeName = name;
        this.storeCategory = categoryName;
        this.restNum = restNum;
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

    public void setRestNum(int restNum) {
        this.restNum = restNum;
    }
}
