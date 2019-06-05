package ac.kr.hansung.foodsharing;

import java.util.HashMap;

public class FoodInfo {
    String[] foodList;
    String[] categoryList;
    int[] foodImgList;

    public FoodInfo() {
         foodList = new String[]{
                 "비빔밥", "불고기", "된장찌개", "김치찌개", "김치전", "떡갈비",
                 "자장면", "짬뽕", "탕수육", "깐풍기", "팔보채", "칠리새우",
                 "파스타", "스테이크", "샐러드", "오믈렛", "햄버거", "피자",
                 "초밥", "가츠동", "우동", "텐동", "라멘", "사시미",
                 "떡볶이", "김밥", "튀김", "순대", "오뎅", "주먹밥"};

         foodImgList = new int[]{
                 R.drawable.image_bibim, R.drawable.image_bulgogi, R.drawable.image_damnzang,
                 R.drawable.image_gimchi, R.drawable.image_gimchijun, R.drawable.image_dduckgalbi,
                 R.drawable.image_zazang, R.drawable.image_zzamgbbong, R.drawable.image_tang,
                 R.drawable.image_kkan, R.drawable.image_palbo, R.drawable.image_chill,
                 R.drawable.image_pasta, R.drawable.image_steak, R.drawable.image_salad,
                 R.drawable.image_omlet, R.drawable.image_hamberger, R.drawable.image_pizza,
                 R.drawable.image_chobob, R.drawable.image_gachdong, R.drawable.image_udong,
                 R.drawable.image_tendong, R.drawable.image_ramen, R.drawable.image_sashimi,
                 R.drawable.image_dduckbok, R.drawable.image_gimbob, R.drawable.image_thigim,
                 R.drawable.image_soondae, R.drawable.image_odang, R.drawable.image_punchbob
         };

        categoryList = new String[]{
                "한식", "중식", "양식", "일식", "분식"
        };
    }

    public int[] getFoodImgList() {
        return foodImgList;
    }

    public void setFoodImgList(int[] foodImgList) {
        this.foodImgList = foodImgList;
    }

    public String[] getFoodList() {
        return foodList;
    }

    public void setFoodList(String[] foodList) {
        this.foodList = foodList;
    }

    public String[] getCategoryList() {
        return categoryList;
    }

    public void setCategoryList(String[] categoryList) {
        this.categoryList = categoryList;
    }
}
