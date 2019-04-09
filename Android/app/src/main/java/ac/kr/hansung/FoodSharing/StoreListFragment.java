package ac.kr.hansung.FoodSharing;


import android.content.Context;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.BaseAdapter;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.Toast;

import java.util.ArrayList;


public class StoreListFragment extends Fragment {
    ListView listView;
    StoreListAdapter adapter;
    View view;


    public StoreListFragment() {
        // Required empty public constructor
    }


    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        view = inflater.inflate(R.layout.fragment_store_list, container, false);

        listView = (ListView) view.findViewById(R.id.listView_store_list);

        adapter = new StoreListAdapter();

        adapter.addItem(new StoreItem("1번 가게", "맛집이죠?", R.drawable.icon_clicked));
        adapter.addItem(new StoreItem("2번 가게", "맛집이죠?!", R.drawable.icon_normal));
        adapter.addItem(new StoreItem("3번 가게", "맛집이죠?!", R.drawable.icon_normal));
        adapter.addItem(new StoreItem("4번 가게", "맛집이죠?!", R.drawable.icon_normal));
        adapter.addItem(new StoreItem("5번 가게", "맛집이죠?!", R.drawable.icon_normal));

        listView.setAdapter(adapter);

        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> adapterView, View view, int position, long id) {
                StoreItem item = (StoreItem) adapter.getItem(position);
                Toast.makeText(getActivity().getApplicationContext(), "선택 : " + item.getStoreName(), Toast.LENGTH_LONG).show();
            }
        });

        return inflater.inflate(R.layout.fragment_store_list, container, false);
    }

    class StoreListAdapter extends BaseAdapter {
        ArrayList<StoreItem> items = new ArrayList<StoreItem>();

        @Override
        public int getCount() {
            return items.size();
        }

        public void addItem(StoreItem item) {
            items.add(item);
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
            StoreItemView view = new StoreItemView(getActivity().getApplicationContext());
            StoreItem item = items.get(position);
            view.setName(item.getStoreName());
            view.setExp(item.getStoreExp());
            view.setIcon(item.getResId());

            return view;
        }
    }


}

