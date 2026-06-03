import React from 'react';
import { StyleSheet, Text, View, TouchableOpacity, Linking, Platform } from 'react-native';
import { Camera, Globe, ExternalLink, ShieldAlert, CheckCircle2, UserPlus } from 'lucide-react-native';

interface LivenessScannerProps {
  mode: 'register' | 'verify';
  onFaceCaptured?: (embedding: number[]) => void;
  onTelemetryUpdate?: (stats: { fps: number; latency: number }) => void;
}

export const LivenessScanner: React.FC<LivenessScannerProps> = ({
  mode,
  onFaceCaptured,
  onTelemetryUpdate
}) => {
  const handleOpenPWA = () => {
    Linking.openURL('https://bharatverify-nhai.surge.sh');
  };

  const handleSimulateAction = () => {
    // Generate a mock 128D face descriptor vector for simulation
    const mockEmbedding = new Array(128).fill(0).map((_, i) => {
      if (mode === 'register') {
        return Math.sin(i * 0.15) * 0.45 + 0.12; // Deterministic mock embedding A
      } else {
        // Matching vector for verification simulation (Euclidean distance < 0.60)
        return Math.sin(i * 0.15) * 0.45 + 0.13; // Slight variation
      }
    });

    if (onFaceCaptured) {
      onFaceCaptured(mockEmbedding);
    }

    if (onTelemetryUpdate) {
      onTelemetryUpdate({ fps: 28, latency: 184 });
    }
  };

  return (
    <View style={styles.container}>
      <View style={styles.alertCard}>
        <ShieldAlert size={36} color="#F59E0B" />
        <Text style={styles.alertTitle}>Edge AI Web Environment Required</Text>
        <Text style={styles.alertDesc}>
          BharatVerify uses high-performance WebGL and WASM deep learning libraries. Standard native mobile clients (Expo Go) lack the browser HTML5 Canvas and video stream drivers required to run these models on the edge.
        </Text>
      </View>

      <Text style={styles.sectionHeader}>TEST OPTIONS FOR EVALUATORS:</Text>

      {/* Button 1: Launch Deployed App */}
      <TouchableOpacity style={styles.actionBtn} onPress={handleOpenPWA}>
        <Globe size={18} color="#0F172A" />
        <Text style={styles.actionBtnText}>Open Hosted Web PWA</Text>
        <ExternalLink size={14} color="#0F172A" style={{ marginLeft: 'auto' }} />
      </TouchableOpacity>
      <Text style={styles.helpText}>
        Launches the production-ready app in your default browser. Supports full camera scanner, liveness checks, and offline PWA install.
      </Text>

      {/* Button 2: Simulate Scanner */}
      <TouchableOpacity style={[styles.actionBtn, styles.secondaryBtn]} onPress={handleSimulateAction}>
        {mode === 'register' ? (
          <UserPlus size={18} color="#F8FAFC" />
        ) : (
          <CheckCircle2 size={18} color="#F8FAFC" />
        )}
        <Text style={styles.secondaryBtnText}>
          {mode === 'register' ? 'Simulate Face Enrollment' : 'Simulate Face Verification'}
        </Text>
      </TouchableOpacity>
      <Text style={styles.helpText}>
        Mocks a successful edge biometric match. Instantly generates a 128D facial template to verify the local storage caching and AWS Sync queue pipelines natively.
      </Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#0F172A',
    borderRadius: 16,
    padding: 20,
    borderWidth: 1,
    borderColor: '#1E293B',
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: 400,
  },
  alertCard: {
    backgroundColor: 'rgba(245, 158, 11, 0.05)',
    borderWidth: 1,
    borderColor: 'rgba(245, 158, 11, 0.15)',
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
    marginBottom: 24,
  },
  alertTitle: {
    color: '#F59E0B',
    fontSize: 14,
    fontWeight: 'bold',
    marginTop: 10,
    marginBottom: 6,
    textAlign: 'center',
  },
  alertDesc: {
    color: '#94A3B8',
    fontSize: 10,
    lineHeight: 14,
    textAlign: 'center',
  },
  sectionHeader: {
    color: '#64748B',
    fontSize: 9,
    fontWeight: 'bold',
    alignSelf: 'flex-start',
    marginBottom: 8,
    letterSpacing: 0.5,
  },
  actionBtn: {
    width: '100%',
    backgroundColor: '#F59E0B',
    borderRadius: 8,
    paddingVertical: 10,
    paddingHorizontal: 14,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginBottom: 4,
  },
  actionBtnText: {
    color: '#0F172A',
    fontWeight: 'bold',
    fontSize: 12,
  },
  secondaryBtn: {
    backgroundColor: '#1E293B',
    borderWidth: 1,
    borderColor: '#334155',
    marginTop: 16,
  },
  secondaryBtnText: {
    color: '#F8FAFC',
    fontWeight: 'bold',
    fontSize: 12,
  },
  helpText: {
    color: '#475569',
    fontSize: 9,
    lineHeight: 12,
    alignSelf: 'flex-start',
    paddingHorizontal: 4,
  },
});
