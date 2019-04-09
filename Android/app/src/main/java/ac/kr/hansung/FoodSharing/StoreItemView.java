package ac.kr.hansung.FoodSharing;

import android.content.Context;
import android.util.AttributeSet;
import android.view.LayoutInflater;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

public class StoreItemView extends LinearLayout{
    TextView storeName;
    TextView storeExp;
    ImageView storeIcon;

    public StoreItemView(Context context) {
        super(context);
        init(context);
    }

    public StoreItemView(Context context, AttributeSet attrs) {
        super(context, attrs);
        init(context);
    }

    public void init(Context context) {
        LayoutInflater inflater = (LayoutInflater) context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        inflater.inflate(R.layout.item_store_list, this, true);

        storeName = (TextView) findViewById(R.id.textView_store_name);
        storeExp = (TextView) findViewById(R.id.textView_store_exp);
        storeIcon = (ImageView) findViewById(R.id.imageView_store_icon);
    }

    public void setName(String name) {
        storeName.setText(name);
    }

    public void setExp(String exp) {
        storeExp.setText(exp);
    }

    public void setIcon(int resId) {
        storeIcon.setImageResource(resId);
    }
}
