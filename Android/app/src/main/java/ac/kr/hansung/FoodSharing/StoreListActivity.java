package ac.kr.hansung.FoodSharing;

import android.content.Context;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.BaseAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.Toast;

import java.util.ArrayList;

public class StoreListActivity extends AppCompatActivity {
    ListView listView;
    StoreListAdapterInAct adapter;
    Button backButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_store_list);

        listView = (ListView) findViewById(R.id.listView_store_list2);
        backButton = (Button) findViewById(R.id.button_store_list_back);
        adapter = new StoreListAdapterInAct();
        listView.setAdapter(adapter);

        backButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });

        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> adapterView, View view, int position, long id) {
                StoreItem item = (StoreItem) adapter.getItem(position);
                Toast.makeText(getApplicationContext(), "선택 : " + item.getStoreName(), Toast.LENGTH_LONG).show();
            }
        });

    }

    @Override
    protected void onStart() {
        super.onStart();
        adapter.addItem(new StoreItem("no.1", "hello", R.drawable.icon_clicked));
        adapter.addItem(new StoreItem("no.2", "bye", R.drawable.icon_normal));
    }
}

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
        view.setExp(item.getStoreExp());
        view.setIcon(item.getResId());
        return view;
    }
}