package ac.kr.hansung.foodsharing;

import android.content.Context;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;

import java.util.ArrayList;

class StoreListAdapterInAct extends BaseAdapter {
    private ArrayList<StoreItem> items = new ArrayList<>();
    private Context context;

    @Override
    public int getCount() {
        return items.size();
    }

    public void addItem(StoreItem item) {
        items.add(item);
    }

    public void addItem(StoreItem[] item) {
        for (int i = 0; i < item.length; i++) {
            items.add(item[i]);
        }
    }

    @Override
    public Object getItem(int position) {
        return items.get(position);
    }

    @Override
    public long getItemId(int position) {
        return position;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        if(context == null) {
            context = parent.getContext();
        }
        StoreItemView view = new StoreItemView(context.getApplicationContext());
        StoreItem item = items.get(position);
        view.setName(item.getStoreName());
        view.setStoreCategory(item.getStoreCategory());
        return view;
    }
}
