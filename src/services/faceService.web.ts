import * as faceapi from '@vladmandic/face-api/dist/face-api.esm.js';

const MODEL_URL = 'https://cdn.jsdelivr.net/npm/@vladmandic/face-api/model/';

class FaceService {
  private modelsLoaded = false;
  private loadingPromise: Promise<void> | null = null;

  public async loadModels(onProgress?: (progress: string) => void): Promise<void> {
    if (this.modelsLoaded) return;
    if (this.loadingPromise) return this.loadingPromise;

    this.loadingPromise = (async () => {
      try {
        if (onProgress) onProgress("Initializing WebGL Backends...");
        
        // Wait for tfjs to be ready and choose the best backend (WebGL > WASM > CPU)
        await faceapi.tf.ready();
        
        if (onProgress) onProgress("Loading SSD Face Detector (5.1MB)...");
        await faceapi.nets.ssdMobilenetv1.loadFromUri(MODEL_URL);
        
        if (onProgress) onProgress("Loading Landmark Predictor (350KB)...");
        await faceapi.nets.faceLandmark68Net.loadFromUri(MODEL_URL);
        
        if (onProgress) onProgress("Loading Face Descriptor Extractor (5.2MB)...");
        await faceapi.nets.faceRecognitionNet.loadFromUri(MODEL_URL);
        
        this.modelsLoaded = true;
        console.log(`[Diagnostic] Active TFJS Backend: ${faceapi.tf.getBackend()}`);
        if (onProgress) onProgress("All models loaded successfully!");
      } catch (e) {
        this.loadingPromise = null;
        console.error("Failed to load face-api models", e);
        throw new Error("Edge AI models could not be loaded offline. Verify your local assets/CDN path.");
      }
    })();

    return this.loadingPromise;
  }

  public isLoaded(): boolean {
    return this.modelsLoaded;
  }

  /**
   * Run face detection, landmark localization, and descriptor extraction on a video/image frame
   */
  public async detectFaceAndLandmarks(
    input: HTMLVideoElement | HTMLCanvasElement | HTMLImageElement
  ): Promise<faceapi.WithFaceDescriptor<faceapi.WithFaceLandmarks<{ detection: faceapi.FaceDetection }, faceapi.FaceLandmarks68>> | null> {
    if (!this.modelsLoaded) {
      await this.loadModels();
    }

    try {
      // Use SsdMobilenetv1Options which is highly robust to shadows and indoor lighting
      const options = new faceapi.SsdMobilenetv1Options({
        minConfidence: 0.25  // Lowered threshold to retain detection during blinks and head turns
      });

      const result = await faceapi.detectSingleFace(input, options)
        .withFaceLandmarks()
        .withFaceDescriptor();

      return result || null;
    } catch (e) {
      console.error("Error running face detection pipeline", e);
      return null;
    }
  }

  /**
   * Compares a live face descriptor (Float32Array) with a registered embedding (number[])
   * Returns a match score between 0.0 (completely different) and 1.0 (identical match)
   * The match is successful if score is above the threshold (typically distance < 0.6 -> score > 0.65)
   */
  public matchFace(liveDescriptor: Float32Array, registeredEmbedding: number[]): { matched: boolean; score: number } {
    if (liveDescriptor.length !== registeredEmbedding.length) {
      return { matched: false, score: 0 };
    }

    // Calculate Euclidean Distance
    let sumSq = 0;
    for (let i = 0; i < liveDescriptor.length; i++) {
      sumSq += Math.pow(liveDescriptor[i] - registeredEmbedding[i], 2);
    }
    const distance = Math.sqrt(sumSq);

    // Map distance to a standard similarity score percentage.
    // Euclidean distance in face recognition typically ranges:
    // 0.0 - 0.4: Extremely similar (same person)
    // 0.4 - 0.6: Similar (likely same person)
    // 0.6+: Different person
    // Threshold is 0.65.
    const threshold = 0.65; // Relaxed from 0.58 to prevent false rejections due to webcam noise, angle tilt, or lighting changes
    const matched = distance < threshold;

    // Convert to a percentage score for user-friendly UI feedback:
    // A distance of 0 -> 100%
    // A distance of 0.65 -> 80% (threshold boundary)
    // A distance of 1.5 -> 0%
    let score = 0;
    if (distance < threshold) {
      // Scale from 100% down to 80%
      score = 1.0 - (distance / threshold) * 0.20;
    } else {
      // Scale from 80% down to 0%
      score = Math.max(0, 0.80 - ((distance - threshold) / (1.5 - threshold)) * 0.80);
    }

    return {
      matched,
      score: parseFloat(score.toFixed(4))
    };
  }
}

export const faceService = new FaceService();
