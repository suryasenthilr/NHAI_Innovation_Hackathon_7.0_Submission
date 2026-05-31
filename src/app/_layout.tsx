import { Slot } from 'expo-router';
import { useEffect } from 'react';
import { Platform } from 'react-native';

export default function RootLayout() {
  useEffect(() => {
    if (Platform.OS === 'web' && typeof window !== 'undefined' && window.location) {
      const hostname = window.location.hostname;
      const protocol = window.location.protocol;
      if (protocol === 'http:' && hostname !== 'localhost' && hostname !== '127.0.0.1' && !hostname.startsWith('192.168.')) {
        window.location.replace(`https://${hostname}${window.location.pathname}${window.location.search}`);
      }
    }
  }, []);

  return <Slot />;
}

