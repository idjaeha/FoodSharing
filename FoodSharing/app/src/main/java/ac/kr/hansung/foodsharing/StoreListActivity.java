package ac.kr.hansung.foodsharing;

import android.content.Context;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.BaseAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.Toast;

import java.util.ArrayList;

import static ac.kr.hansung.foodsharing.InitActivity.foodInfo;

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
                Toast.makeText(getApplicationContext(), "선택 : " + item.getRestId(), Toast.LENGTH_LONG).show();
            }
        });

    }

    @Override
    protected void onStart() {
        super.onStart();

        Intent intent = getIntent();
        /*
        Intent socketIntent = new Intent(this, SocketService.class);

        int flag = intent.getIntExtra("food_num", -1);
        if (flag >= 0  && flag < 5) {
            socketIntent.putExtra("command", "5");
            socketIntent.putExtra("flag", "0");
            socketIntent.putExtra("category", foodInfo.getCategoryList()[flag]);

        } else if (flag >= 10 && flag < 40) {
            socketIntent.putExtra("command", "5");
            socketIntent.putExtra("flag", "1");
            socketIntent.putExtra("food_name", foodInfo.getFoodList()[flag - 10]);
        }
        */
        adapter.addItem(new StoreItem(intent.getStringExtra("rest_name1"), intent.getStringExtra("category_name1"), 100));

    }

}

