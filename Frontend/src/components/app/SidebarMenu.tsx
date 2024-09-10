import {
  BarChartOutlined,
  LogoutOutlined,
  HomeOutlined,
} from "@ant-design/icons";
import { Menu, MenuProps, Modal } from "antd";
import { useState } from "react";
import { useSignOut } from "react-auth-kit";
import { Link, useLocation } from "react-router-dom";

type MenuItem = Required<MenuProps>["items"][number];

const menuItems: MenuItem[] = [
  {
    key: "/home",
    label: <Link to="/home">Home</Link>,
    icon: <HomeOutlined />,
  },
  {
    key: "/dashboard",
    label: <Link to="/dashboard">Dashboard</Link>,
    icon: <BarChartOutlined />,
  },
  {
    key: "/logout",
    label: "Logout",
    icon: <LogoutOutlined />,
  },
];

const SidebarMenu: React.FC = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const signOut = useSignOut();
  const location = useLocation();

  const handleMenuSelect: MenuProps["onSelect"] = ({ key }) => {
    if (key === "/logout") {
      setIsModalOpen(true);
    }
  };

  return (
    <>
      <Menu
        className="sider__menu"
        selectedKeys={[location.pathname]}
        mode="inline"
        theme="dark"
        items={menuItems}
        onSelect={handleMenuSelect}
      />
      <Modal
        title="Are you sure you want to log out?"
        open={isModalOpen}
        closeIcon={null}
        okText="Log Out"
        onOk={() => {
          signOut();
        }}
        onCancel={() => {
          setIsModalOpen(false);
        }}
      >
        <br />
      </Modal>
    </>
  );
};

export default SidebarMenu;
