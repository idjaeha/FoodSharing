package ac.kr.hansung.foodsharing;

import android.content.Context;
import android.util.AttributeSet;
import android.widget.RadioButton;

public class FoodRadioButton extends android.support.v7.widget.AppCompatRadioButton {
    int foodNum;

    public FoodRadioButton(Context context) {
        super(context);
    }

    public FoodRadioButton(Context context, AttributeSet attrs) {
        super(context, attrs);
    }

    public FoodRadioButton(Context context, AttributeSet attrs, int defStyleAttr) {
        super(context, attrs, defStyleAttr);
    }

    public int getFoodNum() {
        return foodNum;
    }

    public void setFoodNum(int foodNum) {
        this.foodNum = foodNum;
    }
}
