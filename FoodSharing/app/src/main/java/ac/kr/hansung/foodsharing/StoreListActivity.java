package ac.kr.hansung.foodsharing;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ListView;
import android.widget.Toast;

public class StoreListActivity extends AppCompatActivity {
    ListView listView;
    StoreListAdapterInAct adapter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_store_list);

        listView = (ListView) findViewById(R.id.listView_store_list2);

        adapter = new StoreListAdapterInAct();
        listView.setAdapter(adapter);


        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> adapterView, View view, int position, long id) {
                StoreItem item = (StoreItem) adapter.getItem(position);
                int restNum = item.getRestNum();
                Intent menuIntent = new Intent(getApplicationContext(), SocketService.class);
                menuIntent.putExtra("command", "7");
                menuIntent.putExtra("rest_num", restNum);
                startService(menuIntent);
                finish();
            }
        });

    }

    @Override
    protected void onStart() {
        super.onStart();

        // 현재 음식점들의 데이터를 가져옵니다.
        Intent intent = getIntent();
        int num = intent.getIntExtra("num", 0);
        for (int idx = 0; idx < num; idx++)
            adapter.addItem(new StoreItem(intent.getStringExtra("rest_name" + idx), intent.getStringExtra("category_name" + idx), intent.getIntExtra("rest_num" + idx, 100)));
    }

}

