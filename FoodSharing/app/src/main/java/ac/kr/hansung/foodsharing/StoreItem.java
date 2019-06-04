package ac.kr.hansung.foodsharing;

public class StoreItem {

    String storeName;
    String storeCategory;
    int restId;

    public StoreItem(String name) {
        storeName = name;
        restId = -1;
    }

    public StoreItem(String name, String categoryName, int restId) {
        storeName = name;
        this.storeCategory = categoryName;
        this.restId = restId;
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

    public int getRestId() {
        return restId;
    }

    public void setRestId(int restId) {
        this.restId = restId;
    }
}
