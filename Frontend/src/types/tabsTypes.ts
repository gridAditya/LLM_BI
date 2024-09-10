export type TargetKey = React.MouseEvent | React.KeyboardEvent | string;
export interface TabItemType {
  label: string;
  children: JSX.Element;
  key: string;
  closable?: boolean;
};
export interface InputAreaProps {
  loading: boolean;
  onSearch: (setQuery: React.Dispatch<React.SetStateAction<string>>, query: string) => void;
}