import { LockOutlined, UserOutlined } from '@ant-design/icons';
import { Alert, Button, Form, Input } from 'antd';
import { useState } from 'react';
import { useIsAuthenticated, useSignIn } from 'react-auth-kit';
import { Navigate, useNavigate } from 'react-router-dom';
import { LoginFormData } from '../../types/LoginFormData';

const LoginForm = () => {
  const signIn = useSignIn();
  const navigate = useNavigate();
  const isAuthenticated = useIsAuthenticated();
  const [loginLoading, setLoginLoading] = useState<boolean>(false);
  const [hasError, setHasError] = useState<boolean>(false);

  const handleFinish = (form: LoginFormData) => {
    setLoginLoading(true);
    setHasError(false);
    if (
      form.username !== import.meta.env.VITE_APP_USERNAME ||
      form.password !== import.meta.env.VITE_APP_PASSWORD
    ) {
      setTimeout(() => {
        setLoginLoading(false);
        setHasError(true);
      }, 1000);
      return;
    }

    const signinConfig = {
      token: import.meta.env.VITE_APP_AUTH_TOKEN || '',
      expiresIn: 43200, // 30 days
      tokenType: 'Bearer',
      authState: {
        username: form.username,
      },
    };

    setTimeout(() => {
      if (signIn(signinConfig)) {
        navigate('/home');
      }
    }, 1000);
  };

  if (isAuthenticated()) {
    return <Navigate to="/home" />;
  } else {
    return (
      <Form
        className="login-form"
        autoComplete="off"
        onFinish={handleFinish}
      >
        {hasError && (
          <Alert
            message={`Invalid username or password! ${
              import.meta.env.REACT_APP_USERNAME
            }`}
            type="error"
            style={{ marginBottom: '1rem' }}
          />
        )}
        <Form.Item
          name="username"
          rules={[{ required: true, message: 'Please input your username!' }]}
        >
          <Input
            className="login-input"
            name="username"
            size="large"
            placeholder="Username"
            prefix={<UserOutlined />}
          />
        </Form.Item>
        <Form.Item
          name="password"
          rules={[{ required: true, message: 'Please input your password!' }]}
        >
          <Input.Password
            className="login-input"
            name="password"
            size="large"
            placeholder="Password"
            prefix={<LockOutlined />}
          />
        </Form.Item>
        <Form.Item className="actions-container">
          <Button
            className="login-button"
            htmlType="submit"
            type="primary"
            size="large"
            loading={loginLoading}
          >
            <h5>Login</h5>
          </Button>
        </Form.Item>
      </Form>
    );
  }
};

export default LoginForm;
