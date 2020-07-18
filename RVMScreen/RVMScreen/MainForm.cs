using MySql.Data.MySqlClient;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace RVMScreen
{
    public partial class MainForm : Form
    {
        int seccount = 0;
        Timer timer,timersec;
        string mysqlconnectionString = "SERVER=localhost;DATABASE=smartduskbin;UID=root;PASSWORD='123';SslMode=none";
        MySqlConnection conn;
        MySqlCommand cmd, cmdsum, cmdsum2, cmdmax, cmdhistory, cmdcount, cmdexecute, cmdtran, cmdinventory;
        MySqlDataReader reader;
        int rowcount = 0,totalbottle,totalcan,totalpaper,tranmade = 0,total2=0;

        private void tabPage1_Click(object sender, EventArgs e)
        {

        }

        private void MainForm_Load(object sender, EventArgs e)
        {
            timersec = new Timer();
            timersec.Interval = 500;
            timersec.Tick += Timersec_Tick;

            pictureBox4.BackColor = Color.LightGreen;
            label22.Text = "Please enter item to recycle.";
        }

        private void Timersec_Tick(object sender, EventArgs e)
        {
            seccount++;

            if(pictureBox4.Visible == true)
            {
                pictureBox4.Visible = false;
                label22.Visible = false;
            }
            else
            {
                pictureBox4.Visible = true;
                label22.Visible = true;
            }
            

            if (seccount == 10)
            {
                timersec.Stop();
                seccount = 0;
                pictureBox4.BackColor = Color.LightGreen;
                label22.Text = "Please enter next item to recycle.";

                pictureBox4.Visible = true;
                label22.Visible = true;
            }
        }

        private void webBrowser1_Navigated(object sender, WebBrowserNavigatedEventArgs e)
        {
            this.webBrowser1.Document.BackColor = Color.Transparent;
        }

        //private void numericUpDown3_ValueChanged(object sender, EventArgs e)
        //{
        //    label20.Text = countPoint().ToString();
        //}

        //private void numericUpDown2_ValueChanged(object sender, EventArgs e)
        //{
        //    label20.Text = countPoint().ToString();
        //}

        //public int countPoint()
        //{
        //    return (int.Parse(numericUpDown1.Value.ToString()) * 500) + (int.Parse(numericUpDown2.Value.ToString()) * 1800) + (int.Parse(numericUpDown3.Value.ToString()) * 2000);
        //}

        //private void numericUpDown1_ValueChanged(object sender, EventArgs e)
        //{
        //    label20.Text = countPoint().ToString();
        //}

        private void button1_Click_1(object sender, EventArgs e)
        {
            //if(countPoint() <= 0)
            //{
            //    MessageBox.Show("Please select at least an item to continue!", "Information", MessageBoxButtons.OK, MessageBoxIcon.Information);
            //    return;
            //}
            //else if (countPoint() > int.Parse(label15.Text))
            //{
            //    MessageBox.Show("Insufficient balance!", "Information", MessageBoxButtons.OK, MessageBoxIcon.Information);
            //    return;
            //}
            //else
            //{
                

            //    cmdexecute.CommandText = "INSERT INTO rvm(itemamount,point,UserEmail,ActionDateTime,isEnd,isScanned) VALUES(0,'" + countPoint().ToString() + "','" + label6.Text + "',NOW(),0,0)";
            //    cmdexecute.ExecuteNonQuery();

            //    cmdexecute.CommandText = "INSERT INTO rvm(UserEmail,ActionDateTime,isEnd,isScanned) VALUES('" + label6.Text + "',NOW(),0,0)";
            //    cmdexecute.ExecuteNonQuery();

            //    numericUpDown1.Value = 0;
            //    numericUpDown2.Value = 0;
            //    numericUpDown3.Value = 0;

            //    totalbottle = 0;
            //    totalcan = 0;
            //    totalpaper = 0;

            //    MessageBox.Show("Your purchase was successful!", "Information", MessageBoxButtons.OK, MessageBoxIcon.Information);
            //}
        }

        private void tabControl1_SelectedIndexChanged(object sender, EventArgs e)
        {
            tabControl1.SelectedTab.BackColor = Color.Green;

            flowLayoutPanel1.Controls.Clear();

            List<Label> alllablel = tabControl1.SelectedTab.Controls.OfType<Label>().ToList();


            for (int i = 0; i < alllablel.Count; i++)
            {
                alllablel[i].ForeColor = Color.White;
            }

            reader = cmdmax.ExecuteReader();

            int maxid = 0, total1 = 0;
            while (reader.Read())
            {
                maxid = int.Parse(reader.GetString("max"));
            }

            reader.Close();

            if (tabControl1.SelectedIndex == 3)
            {
                timer.Stop();
                conn.Close();
                new Form1().Show();
                Hide();
                return;
            }

            reader = cmd.ExecuteReader();


            while (reader.Read())
            {
                label5.Text = reader.GetString("FirstName") + " " + reader.GetString("LastName");
                label6.Text = reader.GetString("EmailAddress");
                label7.Text = reader.GetString("PhoneNumber");
            }

            reader.Close();

            reader = cmdsum.ExecuteReader();

            while (reader.Read())
            {
                if (reader.GetValue(reader.GetOrdinal("total")) != DBNull.Value)
                {
                    total1 = reader.GetInt32("total");
                }
            }

            reader.Close();
            reader = cmdsum2.ExecuteReader();

            while (reader.Read())
            {
                if (reader.GetValue(reader.GetOrdinal("total")) != DBNull.Value)
                {
                    total2 = reader.GetInt32("total");
                }
            }
            reader.Close();
            
            reader = cmdtran.ExecuteReader();

            while (reader.Read())
            {
                tranmade = int.Parse(reader.GetString("transactions"));
            }

            reader.Close();

            flowLayoutPanel1.Controls.Add(new UserControl2("Total Earned Points: " + total2 + Environment.NewLine + "Transactions Made: " + tranmade.ToString() + Environment.NewLine));

            reader = cmdhistory.ExecuteReader();

            while (reader.Read())
            {
                if (int.Parse(reader.GetString("itemamount")) > 0)
                {
                    flowLayoutPanel1.Controls.Add(new HistoryControl("Items Recycled: " + reader.GetString("itemamount") + Environment.NewLine
                   + "Date: " + reader.GetString("ActionDateTime") + Environment.NewLine + "Points Earned: " + reader.GetString("point"), int.Parse(reader.GetString("itemamount"))));
                }
                else
                {
                    flowLayoutPanel1.Controls.Add(new HistoryControl("Date: " + reader.GetString("ActionDateTime") + Environment.NewLine + "Points Spent: " + reader.GetString("point"), int.Parse(reader.GetString("itemamount"))));
                }


                flowLayoutPanel1.Controls.Add(new UserControl1());
            }
            reader.Close();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            
        }

        public MainForm()
        {
            InitializeComponent();

            pictureBox5.BackColor = Color.White;
            pictureBox12.BackColor = Color.Red;
            pictureBox11.BackColor = Color.Yellow;
            pictureBox6.BackColor = Color.LightGreen;

            pictureBox16.BackColor = Color.White;
            pictureBox13.BackColor = Color.Red;
            pictureBox14.BackColor = Color.Yellow;
            pictureBox15.BackColor = Color.LightGreen;

            pictureBox10.BackColor = Color.White;
            pictureBox7.BackColor = Color.Red;
            pictureBox8.BackColor = Color.Yellow;
            pictureBox9.BackColor = Color.LightGreen;

            conn = new MySqlConnection(mysqlconnectionString);
            conn.Open();

            cmdinventory = conn.CreateCommand();
            cmdinventory.CommandType = System.Data.CommandType.Text;

            pictureBox5.BackColor = Color.White;

            pictureBox16.BackColor = Color.White;

            pictureBox10.BackColor = Color.White;

            cmdinventory.CommandText = "SELECT * FROM inventory where Type = 'Bottle'";

            reader = cmdinventory.ExecuteReader();

            while (reader.Read())
            {
                if (int.Parse(reader.GetString("Level")) == 0)
                {
                    pictureBox12.Visible = false;
                    pictureBox11.Visible = false;
                    pictureBox6.Visible = true;
                }
                else if (int.Parse(reader.GetString("Level")) == 1)
                {
                    pictureBox12.Visible = false;
                    pictureBox11.Visible = true;
                    pictureBox6.Visible = false;
                }
                else
                {
                    pictureBox12.Visible = true;
                    pictureBox11.Visible = false;
                    pictureBox6.Visible = false;
                }
            }

            reader.Close();

            cmdinventory.CommandText = "SELECT * FROM inventory where Type = 'Can'";

            reader = cmdinventory.ExecuteReader();

            while (reader.Read())
            {
                if (int.Parse(reader.GetString("Level")) == 0)
                {
                    pictureBox13.Visible = false;
                    pictureBox14.Visible = false;
                    pictureBox15.Visible = true;
                }
                else if (int.Parse(reader.GetString("Level")) == 1)
                {
                    pictureBox13.Visible = false;
                    pictureBox14.Visible = true;
                    pictureBox15.Visible = false;
                }
                else
                {
                    pictureBox13.Visible = true;
                    pictureBox14.Visible = false;
                    pictureBox15.Visible = false;
                }
            }

            reader.Close();

            cmdinventory.CommandText = "SELECT * FROM inventory where Type = 'Box'";

            reader = cmdinventory.ExecuteReader();

            while (reader.Read())
            {
                if (int.Parse(reader.GetString("Level")) == 0)
                {
                    pictureBox7.Visible = false;
                    pictureBox8.Visible = false;
                    pictureBox9.Visible = true;
                }
                else if (int.Parse(reader.GetString("Level")) == 1)
                {
                    pictureBox7.Visible = false;
                    pictureBox8.Visible = true;
                    pictureBox9.Visible = false;
                }
                else
                {
                    pictureBox7.Visible = true;
                    pictureBox8.Visible = false;
                    pictureBox9.Visible = false;
                }
            }

            reader.Close();

            this.Location = Screen.AllScreens[1].Bounds.Location;

            //string strCmdText;
            //strCmdText = @"CD C:\Users\chuan\Desktop\project sampah";
            //System.Diagnostics.Process.Start("CMD.exe", strCmdText);

            //System.Diagnostics.Process process = new System.Diagnostics.Process();
            //System.Diagnostics.ProcessStartInfo startInfo = new System.Diagnostics.ProcessStartInfo();
            //startInfo.WindowStyle = System.Diagnostics.ProcessWindowStyle.Hidden;
            //startInfo.FileName = "cmd.exe";
            //startInfo.Arguments = "/C copy /b Image1.jpg + Archive.rar Image2.jpg";
            //process.StartInfo = startInfo;
            //process.Start();

            tabControl1.SelectedTab.BackColor = Color.Green;
            this.BackColor = Color.Green;
            groupBox1.ForeColor = Color.White;


            cmd = conn.CreateCommand();
            cmd.CommandType = System.Data.CommandType.Text;
            cmdexecute = conn.CreateCommand();
            cmdexecute.CommandType = System.Data.CommandType.Text;
            cmdcount = conn.CreateCommand();
            cmdcount.CommandType = System.Data.CommandType.Text;
            cmdsum = conn.CreateCommand();
            cmdsum.CommandType = System.Data.CommandType.Text;
            cmdsum2 = conn.CreateCommand();
            cmdsum.CommandType = System.Data.CommandType.Text;
            cmdmax = conn.CreateCommand();
            cmdmax.CommandType = System.Data.CommandType.Text;
            cmdhistory = conn.CreateCommand();
            cmdhistory.CommandType = System.Data.CommandType.Text;
            cmdtran = conn.CreateCommand();
            cmdtran.CommandType = System.Data.CommandType.Text;

            cmdmax.CommandText = "SELECT MAX(ID) as max from rvm";
            reader = cmdmax.ExecuteReader();

            int maxid=0,total1=0,total2=0;
            while (reader.Read())
            {
                maxid = int.Parse(reader.GetString("max"));
            }

            reader.Close();


            cmd.CommandText = "SELECT * FROM user WHERE EmailAddress = (SELECT UserEmail FROM rvm where ID = " + maxid + ")";

            

            reader = cmd.ExecuteReader();
            

            while (reader.Read())
            {
                label5.Text = reader.GetString("FirstName") + " " + reader.GetString("LastName");
                label6.Text = reader.GetString("EmailAddress");
                label7.Text = reader.GetString("PhoneNumber");
            }

            cmdsum.CommandText = "SELECT SUM(point) as total from rvm where UserEmail = '" + label6.Text + "' AND itemamount=0";
            cmdsum2.CommandText = "SELECT SUM(point) as total from rvm where UserEmail = '" + label6.Text + "' AND itemamount!=0";

            reader.Close();

            reader = cmdsum.ExecuteReader();

            while (reader.Read())
            {
                if (reader.GetValue(reader.GetOrdinal("total")) != DBNull.Value)
                {
                    total1 = reader.GetInt32("total");
                }
            }

            reader.Close();
            reader = cmdsum2.ExecuteReader();

            while (reader.Read())
            {
                if (reader.GetValue(reader.GetOrdinal("total")) != DBNull.Value)
                {
                    total2 = reader.GetInt32("total");
                }
            }
            reader.Close();

            cmdhistory.CommandText = "SELECT * FROM rvm WHERE UserEmail = (SELECT UserEmail FROM rvm where ID = " + maxid + ") AND itemamount is not null order by ActionDateTime desc";

            reader = cmdhistory.ExecuteReader();
            
            while (reader.Read())
            {
                if(int.Parse(reader.GetString("itemamount")) > 0)
                {
                    flowLayoutPanel1.Controls.Add(new HistoryControl("Items Recycled: " + reader.GetString("itemamount") + Environment.NewLine
                   + "Date: " + reader.GetString("ActionDateTime") + Environment.NewLine + "Points Earned: " + reader.GetString("point"), int.Parse(reader.GetString("itemamount"))));
                }
                else
                {
                    flowLayoutPanel1.Controls.Add(new HistoryControl("Date: " + reader.GetString("ActionDateTime") + Environment.NewLine + "Points Spent: " + reader.GetString("point"), int.Parse(reader.GetString("itemamount"))));
                }


                flowLayoutPanel1.Controls.Add(new UserControl1());
            }
            reader.Close();

            cmdtran.CommandText = "SELECT COUNT(*) as transactions from rvm where UserEmail = '" + label6.Text + "' AND itemamount is not null";
            reader = cmdtran.ExecuteReader();
            
            while (reader.Read())
            {
                tranmade = int.Parse(reader.GetString("transactions"));
            }

            reader.Close();


            label8.Text = (total2 - total1).ToString();
            label15.Text = label8.Text;

            webBrowser1.Navigate("http://192.168.43.10:8080/smartduskbin/get_image.php?eid=" + label6.Text);

            timer = new Timer();
            timer.Interval = 1000;
            timer.Tick += Timer_Tick;
            timer.Start();

            List<Label> alllablel = tabControl1.SelectedTab.Controls.OfType<Label>().ToList();


            for (int i = 0; i < alllablel.Count; i++)
            {
                alllablel[i].ForeColor = Color.White;
            }
        }

        private void Timer_Tick(object sender, EventArgs e)
        {
            cmdinventory.CommandText = "SELECT * FROM inventory where Type = 'Bottle'";
            
            reader = cmdinventory.ExecuteReader();

            while (reader.Read())
            {
                if(int.Parse(reader.GetString("Level")) == 0)
                {
                    pictureBox12.Visible = false;
                    pictureBox11.Visible = false;
                    pictureBox6.Visible = true;
                }
                else if(int.Parse(reader.GetString("Level")) == 1)
                {
                    pictureBox12.Visible = false;
                    pictureBox11.Visible = true;
                    pictureBox6.Visible = false;
                }
                else
                {
                    pictureBox12.Visible = true;
                    pictureBox11.Visible = false;
                    pictureBox6.Visible = false;
                }
            }

            reader.Close();

            cmdinventory.CommandText = "SELECT * FROM inventory where Type = 'Can'";

            reader = cmdinventory.ExecuteReader();

            while (reader.Read())
            {
                if (int.Parse(reader.GetString("Level")) == 0)
                {
                    pictureBox13.Visible = false;
                    pictureBox14.Visible = false;
                    pictureBox15.Visible = true;
                }
                else if (int.Parse(reader.GetString("Level")) == 1)
                {
                    pictureBox13.Visible = false;
                    pictureBox14.Visible = true;
                    pictureBox15.Visible = false;
                }
                else
                {
                    pictureBox13.Visible = true;
                    pictureBox14.Visible = false;
                    pictureBox15.Visible = false;
                }
            }

            reader.Close();

            cmdinventory.CommandText = "SELECT * FROM inventory where Type = 'Box'";

            reader = cmdinventory.ExecuteReader();

            while (reader.Read())
            {
                if (int.Parse(reader.GetString("Level")) == 0)
                {
                    pictureBox7.Visible = false;
                    pictureBox8.Visible = false;
                    pictureBox9.Visible = true;
                }
                else if (int.Parse(reader.GetString("Level")) == 1)
                {
                    pictureBox7.Visible = false;
                    pictureBox8.Visible = true;
                    pictureBox9.Visible = false;
                }
                else
                {
                    pictureBox7.Visible = true;
                    pictureBox8.Visible = false;
                    pictureBox9.Visible = false;
                }
            }

            reader.Close();

            cmdcount.CommandText = "SELECT COUNT(*) as rowcount FROM item";


            reader = cmdcount.ExecuteReader();


            int previousCount = rowcount;
            int total1 = 0, total2 = 0;

            while (reader.Read())
            {
                rowcount = int.Parse(reader.GetString("rowcount"));
            }

            reader.Close();

            cmdmax.CommandText = "SELECT MAX(itemid) as max from item";
            reader = cmdmax.ExecuteReader();

            int maxid = 0;
            while (reader.Read())
            {
                maxid = int.Parse(reader.GetString("max"));
            }

            reader.Close();

            reader = cmdsum.ExecuteReader();

            while (reader.Read())
            {
                if (reader.GetValue(reader.GetOrdinal("total")) != DBNull.Value)
                {
                    total1 = reader.GetInt32("total");
                }
            }

            reader.Close();
            reader = cmdsum2.ExecuteReader();

            while (reader.Read())
            {
                if (reader.GetValue(reader.GetOrdinal("total")) != DBNull.Value)
                {
                    total2 = reader.GetInt32("total");
                }
            }
            reader.Close();

            label8.Text = (total2 - total1).ToString();
            label15.Text = label8.Text;


            reader.Close();

            if (previousCount > 0)
            {
                if (rowcount != previousCount)
                {
                    cmdcount.CommandText = "SELECT * FROM item WHERE itemid = " + maxid;
                    
                    reader = cmdcount.ExecuteReader();

                    while (reader.Read())
                    {
                        if(reader.GetString("type") == "bottle")
                        {
                            totalbottle++;
                        }
                        else if (reader.GetString("type") == "tin")
                        {
                            totalcan++;
                        }
                        else if (reader.GetString("type") == "box")
                        {
                            totalpaper++;
                        }
                    }

                    label11.Text = totalbottle.ToString();
                    label10.Text = totalcan.ToString();
                    label9.Text = totalpaper.ToString();

                    timersec.Start();
                    pictureBox4.BackColor = Color.Red;
                    label22.Text = "Item processing...";

                    reader.Close();
                }
            }

            
        }

        private void label1_Click(object sender, EventArgs e)
        {

        }
    }
}
