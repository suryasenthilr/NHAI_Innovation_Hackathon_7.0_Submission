class FaceService {
  private modelsLoaded = false;

  public async loadModels(onProgress?: (progress: string) => void): Promise<void> {
    this.modelsLoaded = true;
    if (onProgress) onProgress("Running native fallback mode...");
  }

  public isLoaded(): boolean {
    return this.modelsLoaded;
  }

  public async detectFaceAndLandmarks(input: any): Promise<null> {
    return null;
  }

  /**
   * Compares a live face descriptor with a registered embedding (Euclidean Distance calculation)
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

    const threshold = 0.65;
    const matched = distance < threshold;

    let score = 0;
    if (distance < threshold) {
      score = 1.0 - (distance / threshold) * 0.20;
    } else {
      score = Math.max(0, 0.80 - ((distance - threshold) / (1.5 - threshold)) * 0.80);
    }

    return {
      matched,
      score: parseFloat(score.toFixed(4))
    };
  }
}

export const faceService = new FaceService();
