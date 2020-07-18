using MySql.Data.MySqlClient;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Security.Policy;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace RVMScreen
{
    public partial class Form1 : Form
    {
        Timer timer;
        string mysqlconnectionString = "SERVER=localhost;DATABASE=smartduskbin;UID=root;PASSWORD='123';SslMode=none";
        MySqlConnection conn;
        MySqlCommand cmd;
        MySqlDataReader reader;
        int rowcount = 0;
        DateTime dt = DateTime.Now;
        int days = DateTime.DaysInMonth(DateTime.Now.Year, DateTime.Now.Month);
        List<DateCLass> dateList;

        public Form1()
        {
            InitializeComponent();
            


            this.Location = Screen.AllScreens[1].Bounds.Location;


            dateList = new List<DateCLass>();

            timer = new Timer();
            timer.Interval = 1000;
            timer.Tick += Timer_Tick;
            timer.Start();
            
            label1.ForeColor = Color.White;

            conn = new MySqlConnection(mysqlconnectionString);
            conn.Open();

            cmd = conn.CreateCommand();
            cmd.CommandType = System.Data.CommandType.Text;

            this.BackColor = Color.Green;

            chart1.Series.Clear();

            chart1.Series.Add("Total Items Recycled");

            chart1.ChartAreas[0].AxisX.Interval = 1;

            cmd.CommandText = "SELECT SUM(itemamount) AS DailyTransaction,DATE(ActionDateTime) AS ActionDate from rvm where itemamount is not null AND itemamount > 0 GROUP BY DATE(ActionDateTime)";

            reader = cmd.ExecuteReader();

            while (reader.Read())
            {
                dateList.Add(new DateCLass()
                {
                    date = DateTime.Parse(reader.GetString("ActionDate")).ToShortDateString(),
                    count = int.Parse(reader.GetString("DailyTransaction"))
                });
            }

            for (int i = 1; i < days + 1; i++)
            {
                DateCLass dc = dateList.FirstOrDefault(x => x.date == new DateTime(dt.Year, dt.Month, i).ToShortDateString());
                if (dc != null)
                {
                    chart1.Series[0].Points.AddXY(dc.date, dc.count);
                }
                else
                {
                    chart1.Series[0].Points.AddXY(new DateTime(dt.Year, dt.Month, i).ToShortDateString(), 0);
                }
            }

            reader.Close();
        }

        private void Timer_Tick(object sender, EventArgs e)
        {
            cmd.CommandText = "SELECT COUNT(*) as rowcount FROM RVM where itemamount > 0 OR itemamount is null";


            reader = cmd.ExecuteReader();


            int previousCount = rowcount;
            while (reader.Read())
            {
                rowcount = int.Parse(reader.GetString("rowcount"));
            }

            if (previousCount > 0)
            {
                if (rowcount != previousCount)
                {
                    timer.Stop();
                    conn.Close();
                    new MainForm().Show();
                    Hide();
                    return;
                }
            }

            reader.Close();

            cmd.CommandText = "SELECT SUM(itemamount) AS DailyTransaction,DATE(ActionDateTime) AS ActionDate from rvm where itemamount is not null AND itemamount > 0 GROUP BY DATE(ActionDateTime)";

            reader = cmd.ExecuteReader();

            chart1.Series[0].Points.Clear();
            dateList.Clear();

            while (reader.Read())
            {
                dateList.Add(new DateCLass()
                {
                    date = DateTime.Parse(reader.GetString("ActionDate")).ToShortDateString(),
                    count = int.Parse(reader.GetString("DailyTransaction"))
                });
            }

            for (int i = 1; i < days + 1; i++)
            {
                DateCLass dc = dateList.FirstOrDefault(x => x.date == new DateTime(dt.Year, dt.Month, i).ToShortDateString());
                if (dc != null)
                {
                    chart1.Series[0].Points.AddXY(dc.date, dc.count);
                }
                else
                {
                    chart1.Series[0].Points.AddXY(new DateTime(dt.Year, dt.Month, i).ToShortDateString(), 0);
                }
            }

            reader.Close();
        }
    }
}
