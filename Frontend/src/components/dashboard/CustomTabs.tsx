import { createContext, useContext, useEffect, useRef, useState } from "react";
import { Tabs } from "antd";
import ChartsLayout from "./ChartsLayout";
import SqlCard from "./SqlCard";
import { TabItemType, TargetKey } from "../../types/tabsTypes";
import { ApiContext } from "../app/Layout";
import { useNavigate } from "react-router-dom";

export const TabsContext = createContext<{ add: () => void } | null>(null);
const initialItems: TabItemType[] = [
  {
    label: "Tab",
    children: (
      <>
        <ChartsLayout keyIndex={"newTab0"} />
      </>
    ),
    key: "newTab0",
    closable: false,
  },
];

const CustomTabs: React.FC = () => {
  const { chartDataFromApi } = useContext(ApiContext);
  const [activeKey, setActiveKey] = useState(initialItems[0].key);
  const [items, setItems] = useState<TabItemType[]>(initialItems);
  const navigate =     useNavigate();

  const [ChartsLayoutState, setChartsLayoutState] = useState<any>([]);
  const newTabIndex = useRef(0);

  const onChange = (newActiveKey: string) => {
    setActiveKey(newActiveKey);
  };

  const add = () => {
    const newActiveKey = `newTab${++newTabIndex.current}`;
    const newPanes: TabItemType[] = [...items];
    newPanes.push({
      label: `Tab ${newTabIndex.current}`,
      children: (
        <>
          <ChartsLayout keyIndex={activeKey} />
        </>
      ),
      key: newActiveKey,
    });
    setItems(newPanes);
    setActiveKey(newActiveKey);
  };

  const remove = (targetKey: TargetKey) => {
    let newActiveKey = activeKey;
    let lastIndex = -1;
    items.forEach((item, i) => {
      if (item.key === targetKey) {
        lastIndex = i - 1;
      }
    });
    const newPanes = items.filter((item) => item.key !== targetKey);
    if (newPanes.length && newActiveKey === targetKey) {
      if (lastIndex >= 0) {
        newActiveKey = newPanes[lastIndex].key;
      } else {
        newActiveKey = newPanes[0].key;
      }
    }
    setItems(newPanes);
    setActiveKey(newActiveKey);
  };

  const onEdit = (
    targetKey: React.MouseEvent | React.KeyboardEvent | string,
    action: "add" | "remove"
  ) => {
    if (action === "add") {
      add();
    } else {
      remove(targetKey);
    }
  };

  useEffect(() => {
    if (!!!chartDataFromApi) {
      navigate('/home')
    }
  }, [])
  
  return (
    <>
      <TabsContext.Provider value={{ add }}>
        <Tabs
          hideAdd
          type="editable-card"
          onChange={onChange}
          activeKey={activeKey ? activeKey : ""}
          onEdit={onEdit}
          items={items}
          // style={{ height: '50vh' }}
        />
      </TabsContext.Provider>
      <SqlCard keyIndex={activeKey} />
    </>
  );
};

export default CustomTabs;
