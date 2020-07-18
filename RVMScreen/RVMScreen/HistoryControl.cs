using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace RVMScreen
{
    public partial class HistoryControl : UserControl
    {
        public HistoryControl(string text,int items)
        {
            InitializeComponent();

            label1.Text = text;
            label1.ForeColor = Color.White;

            if(items > 0)
            {
                pictureBox1.Image = Image.FromFile(@"C:\Users\chuan\source\repos\RVMScreen\RVMScreen\Images\plastic.png");
            }
            else
            {
                pictureBox1.Image = Image.FromFile(@"C:\Users\chuan\source\repos\RVMScreen\RVMScreen\Images\purchase.jpg");
            }
            
        }
    }
}
