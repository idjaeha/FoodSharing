package ac.kr.hansung.FoodSharing;

public class StoreItem {

    String storeName;
    String storeExp;
    int resId;

    public StoreItem(String name, String exp) {
        storeName = name;
        storeExp = exp;
    }

    public StoreItem(String name, String exp, int resId) {
        storeName = name;
        storeExp = exp;
        this.resId = resId;
    }

    public String getStoreName() {
        return storeName;
    }

    public void setStoreName(String storeName) {
        this.storeName = storeName;
    }

    public String getStoreExp() {
        return storeExp;
    }

    public void setStoreExp(String storeExp) {
        this.storeExp = storeExp;
    }

    public int getResId() {
        return resId;
    }

    public void setResId(int resId) {
        this.resId = resId;
    }
}
