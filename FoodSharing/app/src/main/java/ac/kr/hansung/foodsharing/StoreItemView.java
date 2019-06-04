package ac.kr.hansung.foodsharing;

import android.content.Context;
import android.util.AttributeSet;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

public class StoreItemView extends LinearLayout {
    TextView storeName;
    TextView storeCategory;

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
        storeCategory = (TextView) findViewById(R.id.textView_store_category);
    }

    public void setName(String name) {
        storeName.setText(name);
    }

    public void setStoreCategory(String storeCategory) {
        this.storeCategory.setText(storeCategory);
    }
}

