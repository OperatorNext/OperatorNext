# Frontend Development Guide

This guide provides comprehensive information about frontend development in OperatorNext.

## Development Environment

### Prerequisites

- Node.js 18+ (LTS recommended)
- pnpm 10+
- Docker & Docker Compose
- Git
- VS Code (recommended)

### VS Code Extensions

```json
{
  "recommendations": [
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "bradlc.vscode-tailwindcss",
    "ms-vscode.vscode-typescript-next",
    "prisma.prisma",
    "biomejs.biome"
  ]
}
```

### Environment Setup

1. Install dependencies:
```bash
pnpm install
```

2. Set up environment variables:
```bash
cp .env.local.example .env.local
```

3. Start development services:
```bash
docker-compose up -d
```

4. Start development server:
```bash
pnpm dev
```

## Project Structure

```
frontend/
├── apps/
│   └── web/                 # Next.js application
│       ├── app/             # App router pages
│       ├── components/      # React components
│       ├── hooks/           # Custom hooks
│       ├── lib/             # Utilities
│       ├── styles/          # Global styles
│       └── types/           # TypeScript types
├── packages/
│   ├── ui/                 # Shared UI components
│   ├── api/                # API client
│   ├── auth/               # Authentication
│   ├── config/             # Configuration
│   ├── database/           # Database schema
│   ├── i18n/              # Internationalization
│   ├── mail/              # Email templates
│   └── utils/             # Shared utilities
└── tooling/                # Build and dev tools
```

## Coding Standards

### TypeScript

```typescript
// Use interfaces for objects
interface User {
  id: string;
  name: string;
  email: string;
  role: UserRole;
}

// Use enums for fixed values
enum UserRole {
  Admin = 'admin',
  User = 'user',
  Guest = 'guest'
}

// Use type for unions and complex types
type ApiResponse<T> = {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
  };
};
```

### React Components

```typescript
// Use functional components
const UserProfile: React.FC<UserProfileProps> = ({ user }) => {
  // Use hooks at the top
  const [isEditing, setIsEditing] = useState(false);
  const { t } = useTranslation();

  // Extract complex logic to hooks
  const { mutate } = useUpdateUser();

  // Use early returns
  if (!user) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>{user.name}</h1>
      {/* ... */}
    </div>
  );
};
```

### Styling

```typescript
// Use Tailwind CSS with consistent patterns
const Button: React.FC<ButtonProps> = ({ variant = 'primary', ...props }) => {
  const baseStyles = 'px-4 py-2 rounded-md font-medium';
  const variantStyles = {
    primary: 'bg-blue-500 text-white hover:bg-blue-600',
    secondary: 'bg-gray-200 text-gray-800 hover:bg-gray-300'
  };

  return (
    <button
      className={cn(baseStyles, variantStyles[variant])}
      {...props}
    />
  );
};
```

## State Management

### Server State

```typescript
// Use React Query for server state
const useUsers = () => {
  return useQuery({
    queryKey: ['users'],
    queryFn: async () => {
      const response = await fetch('/api/users');
      return response.json();
    }
  });
};

// Use mutations for updates
const useUpdateUser = () => {
  return useMutation({
    mutationFn: async (data: UpdateUserData) => {
      const response = await fetch('/api/users', {
        method: 'PUT',
        body: JSON.stringify(data)
      });
      return response.json();
    }
  });
};
```

### Client State

```typescript
// Use Zustand for client state
interface UIStore {
  theme: 'light' | 'dark';
  setTheme: (theme: 'light' | 'dark') => void;
}

const useUIStore = create<UIStore>((set) => ({
  theme: 'light',
  setTheme: (theme) => set({ theme })
}));
```

## API Integration

### API Client

```typescript
// Use typed API client
const api = createClient<ApiSchema>({
  baseUrl: '/api',
  headers: {
    'Content-Type': 'application/json'
  }
});

// Use with React Query
const useUser = (id: string) => {
  return useQuery({
    queryKey: ['user', id],
    queryFn: () => api.users.get(id)
  });
};
```

### WebSocket Integration

```typescript
// Use typed WebSocket client
const useWebSocket = <T>(url: string) => {
  const socket = useRef<WebSocket>();
  const [data, setData] = useState<T>();

  useEffect(() => {
    socket.current = new WebSocket(url);
    socket.current.onmessage = (event) => {
      setData(JSON.parse(event.data));
    };

    return () => {
      socket.current?.close();
    };
  }, [url]);

  return data;
};
```

## Testing

### Unit Tests

```typescript
// Use Vitest for unit tests
describe('Button', () => {
  it('renders correctly', () => {
    const { getByText } = render(
      <Button>Click me</Button>
    );
    expect(getByText('Click me')).toBeInTheDocument();
  });

  it('handles click events', () => {
    const onClick = vi.fn();
    const { getByText } = render(
      <Button onClick={onClick}>Click me</Button>
    );
    fireEvent.click(getByText('Click me'));
    expect(onClick).toHaveBeenCalled();
  });
});
```

### Integration Tests

```typescript
// Use Playwright for integration tests
test('user can login', async ({ page }) => {
  await page.goto('/login');
  await page.fill('[name=email]', 'test@example.com');
  await page.fill('[name=password]', 'password');
  await page.click('button[type=submit]');
  await expect(page).toHaveURL('/dashboard');
});
```

## Performance

### Code Splitting

```typescript
// Use dynamic imports for code splitting
const DashboardChart = dynamic(() => import('./DashboardChart'), {
  loading: () => <div>Loading chart...</div>,
  ssr: false
});
```

### Image Optimization

```typescript
// Use Next.js Image component
import Image from 'next/image';

const Avatar = ({ user }) => (
  <Image
    src={user.avatar}
    alt={user.name}
    width={40}
    height={40}
    className="rounded-full"
  />
);
```

### Performance Monitoring

```typescript
// Use Web Vitals
export function reportWebVitals(metric: NextWebVitalsMetric) {
  console.log(metric);
  // Send to analytics
}
```

## Internationalization

### Translation Setup

```typescript
// Use next-intl for translations
const messages = {
  en: {
    common: {
      welcome: 'Welcome, {name}!',
      error: 'Something went wrong'
    }
  },
  zh: {
    common: {
      welcome: '欢迎，{name}！',
      error: '出错了'
    }
  }
};
```

### Usage in Components

```typescript
// Use translations in components
const Welcome: React.FC<{ name: string }> = ({ name }) => {
  const t = useTranslations('common');
  return <h1>{t('welcome', { name })}</h1>;
};
```

## Deployment

### Build Process

```bash
# Build for production
pnpm build

# Analyze bundle
pnpm analyze

# Type check
pnpm type-check
```

### Environment Configuration

```typescript
// Use environment validation
import { z } from 'zod';

const envSchema = z.object({
  NEXT_PUBLIC_API_URL: z.string().url(),
  NEXT_PUBLIC_WS_URL: z.string().url(),
  NEXT_PUBLIC_GA_ID: z.string().optional()
});

export const env = envSchema.parse(process.env);
```

## Additional Resources

- [Component Library Documentation](../components/index.md)
- [API Integration Guide](../api/integration.md)
- [Performance Guide](../performance/index.md)
- [Testing Guide](../testing/index.md)
- [Deployment Guide](../deployment/index.md) 