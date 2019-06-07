package ac.kr.hansung.foodsharing;

import android.content.Context;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import static ac.kr.hansung.foodsharing.InitActivity.mobileInfo;

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

    public void sortItems() {
        /*
        item들을 사용자와의 거리 순으로 오름차순 정렬합니다.
         */
        ArrayList<StoreItem> tmp = new ArrayList<>();
        int[] lengths = new int[items.size()];

        // 거리를 계산하여 리스트에 넣습니다.
        for (int idx = 0; idx < items.size(); idx++) {
            int length = (mobileInfo.getX() - items.get(idx).getX()) * (mobileInfo.getX() - items.get(idx).getX()) +
                    (mobileInfo.getY() - items.get(idx).getY()) * (mobileInfo.getY() - items.get(idx).getY());
            lengths[idx] = length;
        }

        // 계산된 거리 값을 통해 정렬합니다.
        for (int num = 0; num < items.size(); num++) {

            //가장 작은 값의 idx를 구합니다.
            int minIdx = 0;
            int minValue = 999999999;
            for (int idx = 0; idx < items.size(); idx++) {
                if (lengths[idx] < minValue) {
                    minValue = lengths[idx];
                    minIdx = idx;
                }
            }
            lengths[minIdx] = 999999999;
            tmp.add(items.get(minIdx));
        }

        items = tmp;
    }
}
