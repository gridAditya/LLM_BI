import { Button, Input } from "antd";
import { SendOutlined } from "@ant-design/icons";
import { InputAreaProps } from "../../types/tabsTypes";
import { useState } from "react";

const InputArea = ({
  loading,
  onSearch
}: InputAreaProps) => {

  const [query, setQuery] = useState<string>("");
const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    onSearch(setQuery, query);
  }
};
  return (
    <>
      <Input.TextArea
        value={query}
        onChange={(event: React.ChangeEvent<HTMLTextAreaElement>) =>
          !loading && setQuery(event.target.value)
        }
        onKeyDown={handleKeyDown}
        autoSize={{ minRows: 1, maxRows: 3 }}
        placeholder="What are the top 10 trending hashtags this week?"
      />
      <Button type="primary" onClick={()=>onSearch(setQuery, query)} icon={<SendOutlined />} />
    </>
  );
};

export default InputArea