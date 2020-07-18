using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Net.Mail;

namespace RVMScreen
{
    public partial class UserControl2 : UserControl
    {
        public UserControl2(string text)
        {
            InitializeComponent();
            label1.Text = text;
            this.ForeColor = Color.White;
        }
    }
}
