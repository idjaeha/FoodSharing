package ac.kr.hansung.foodsharing;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.TextView;

public class MenuActivity extends AppCompatActivity {
    RadioGroup radioGroupMenu;
    TextView textViewMenuTitle;
    Button buttonFoodSelect;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_menu);

        radioGroupMenu = findViewById(R.id.radioGroup_menu);
        textViewMenuTitle = findViewById(R.id.textView_menu_title);
        buttonFoodSelect = findViewById(R.id.button_food_select);

        buttonFoodSelect.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                int id = radioGroupMenu.getCheckedRadioButtonId();
                FoodRadioButton tmpRadioButton = findViewById(id);
                Intent chatIntent = new Intent(getApplicationContext(), SocketService.class);
                chatIntent.putExtra("command", "9");
                chatIntent.putExtra("food_num", tmpRadioButton.getFoodNum());
                startService(chatIntent);
                finish();
            }
        });
    }

    public MenuActivity() {
        super();
    }

    @Override
    protected void onStart() {
        super.onStart();

        Intent recvIntent = getIntent();
        int num = recvIntent.getIntExtra("num", 0);
        String title = recvIntent.getStringExtra("title");
        textViewMenuTitle.setText(title);
        for (int i = 0; i < num; i++) {
            String foodName = recvIntent.getStringExtra("food_name" + i);
            int foodNum = recvIntent.getIntExtra("food_num"+i, -1);
            FoodRadioButton tmpRadioBtn = new FoodRadioButton(this);
            tmpRadioBtn.setFoodNum(foodNum);
            tmpRadioBtn.setText(foodName);
            tmpRadioBtn.setTextSize(20);
            Log.d("MenuActivity", "foodNum : " + Integer.toString(foodNum));
            Log.d("MenuActivity", "foodName :" + foodName);
            radioGroupMenu.addView(tmpRadioBtn);
        }
    }
}
