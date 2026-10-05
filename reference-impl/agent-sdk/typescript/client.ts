/**
 * OpenTrade Agent SDK — TypeScript client for the OpenTrade Protocol.
 *
 * Enables AI agents to search, negotiate, and complete transactions
 * across all federated OpenTrade nodes using a single unified API.
 *
 * @example
 * ```typescript
 * import { Client } from '@opentrade/agent-sdk';
 *
 * const client = new Client({ apiKey: 'your_api_key' });
 *
 * const results = await client.search({
 *   query: 'Jones Flagship 158',
 *   filters: { category: 'snowboard', condition: ['good', 'like_new'] },
 *   buyerLocation: { lat: 55.75, lon: 37.61 },
 * });
 *
 * for (const listing of results.results) {
 *   console.log(`${listing.product.brand} ${listing.product.model} - ${listing.totalLandedCost.total} RUB`);
 * }
 * ```
 */

export interface Location {
  lat: number;
  lon: number;
  geohash?: string;
  city?: string;
  country?: string;
}

export interface SearchFilters {
  category?: string;
  brand?: string[];
  condition?: Condition[];
  priceMin?: number;
  priceMax?: number;
  sellerMinRating?: number;
  sellerMaxDisputeRate?: number;
  aiConfidenceMin?: number;
  hasSerialVerification?: boolean;
  yearMin?: number;
  yearMax?: number;
}

export enum Condition {
  New = 'new',
  LikeNew = 'like_new',
  Good = 'good',
  Fair = 'fair',
  Poor = 'poor',
}

export enum SortOrder {
  Relevance = 'relevance_score',
  TotalCostAsc = 'total_cost_asc',
  TotalCostDesc = 'total_cost_desc',
  Newest = 'newest',
  SellerRatingDesc = 'seller_rating_desc',
}

export interface SearchResult {
  listingId: string;
  nodeId: string;
  product: {
    category: string;
    brand: string;
    model: string;
    condition: {
      overallGrade: string;
      descriptionAccuracy?: number;
    };
  };
  pricing: {
    askPrice: { amount: number; currency: string };
  };
  totalLandedCost: {
    product: number;
    shipping: number;
    insurance: number;
    platformFee: number;
    total: number;
  };
  seller: {
    did: string;
    trustScore: number;
  };
  aiConfidence: number;
}

export interface SearchResponse {
  results: SearchResult[];
  totalEstimated: number;
  nextCursor?: string;
  searchMetadata: {
    queryUnderstoodAs?: string;
    semanticFallbackUsed: boolean;
    executionTimeMs: number;
  };
}

export interface SearchRequest {
  query: string;
  filters?: SearchFilters;
  buyerLocation?: Location;
  sort?: SortOrder;
  limit?: number;
  cursor?: string;
  includeLogistics?: boolean;
  currency?: string;
}

export interface Offer {
  offerId: string;
  listingId: string;
  buyerDid: string;
  sellerDid: string;
  offerPrice: { amount: number; currency: string };
  message: string;
  status: 'pending' | 'accepted' | 'rejected' | 'countered' | 'expired';
  createdAt: string;
  expiresAt: string;
  signature: string;
}

export interface OfferRequest {
  offerPrice: number;
  currency: string;
  message: string;
  expiresIn: string;
  buyerDid: string;
  paymentMethod: 'escrow' | 'direct' | 'crypto';
}

export interface OfferResponse {
  action: 'accept' | 'reject' | 'counter';
  counterOfferPrice?: number;
  counterCurrency?: string;
  counterExpiresIn?: string;
  counterMessage?: string;
}

export interface Escrow {
  escrowId: string;
  listingId: string;
  buyerDid: string;
  sellerDid: string;
  status: string;
  amounts: {
    product: { amount: number; currency: string };
    shipping: { amount: number; currency: string };
    insurance: { amount: number; currency: string };
    platformFee: { amount: number; currency: string };
    total: { amount: number; currency: string };
  };
  timeline: Array<{ event: string; at: string }>;
  pinCode: string;
  inspectionPeriodExpires: string;
  disputeWindowExpires: string;
}

export interface EscrowCreateRequest {
  listingId: string;
  buyerDid: string;
  sellerDid: string;
  shippingMethod: string;
  insurance: boolean;
  paymentMethod: 'bank_transfer' | 'card' | 'crypto';
}

export interface TrustScore {
  overall: number;
  components: {
    identityVerification: number;
    transactionCompletion: number;
    disputeResolution: number;
    descriptionAccuracy: number;
    shippingSpeed: number;
  };
  totalTransactions: number;
  disputeRate: number;
  avgResponseTimeMin: number;
  returnRate: number;
  verifiedIdentity: boolean;
  verifiedSince: string;
  decay: string;
  categoryExpertise: Record<string, { deals: number; score: number }>;
}

export interface LogisticsRequest {
  origin: Location;
  destination: Location;
  dimensions: {
    l: number;
    w: number;
    h: number;
    weight: number;
  };
  declaredValue: number;
  insurance: boolean;
}

export interface LogisticsResponse {
  options: Array<{
    carrier: string;
    service: string;
    cost: number;
    insuranceCost: number;
    daysMin: number;
    daysMax: number;
    tracking: boolean;
  }>;
  totalLandedCost: {
    product: number;
    shipping: number;
    insurance: number;
    platformFee: number;
    total: number;
  };
}

export interface ClientConfig {
  apiKey?: string;
  didJwt?: string;
  baseUrl?: string;
}

export class Client {
  private apiKey: string | undefined;
  private didJwt: string | undefined;
  private baseUrl: string;

  constructor(config: ClientConfig = {}) {
    this.apiKey = config.apiKey;
    this.didJwt = config.didJwt;
    this.baseUrl = (config.baseUrl || 'https://api.opentradeprotocol.com/v1').replace(/\/$/, '');
  }

  private headers(auth?: string): Record<string, string> {
    const h: Record<string, string> = { 'Content-Type': 'application/json' };
    const token = auth || this.apiKey || this.didJwt;
    if (token) h['Authorization'] = `Bearer ${token}`;
    return h;
  }

  private async request<T>(path: string, options?: RequestInit): Promise<T> {
    const url = `${this.baseUrl}${path}`;
    const response = await fetch(url, {
      ...options,
      headers: { ...this.headers(), ...(options?.headers as Record<string, string> || {}) },
    });
    if (!response.ok) {
      const error = await response.text();
      throw new Error(`OpenTrade API error ${response.status}: ${error}`);
    }
    return response.json();
  }

  /**
   * Search across all federated OpenTrade nodes.
   */
  async search(params: SearchRequest): Promise<SearchResponse> {
    const body: any = { query: params.query };
    if (params.filters) body.filters = params.filters;
    if (params.buyerLocation) body.buyer_location = params.buyerLocation;
    if (params.sort) body.sort = params.sort;
    body.limit = Math.min(params.limit || 20, 100);
    if (params.cursor) body.cursor = params.cursor;
    if (params.includeLogistics !== undefined) body.include_logistics = params.includeLogistics;
    if (params.currency) body.currency = params.currency;

    const data = await this.request<any>('/search', {
      method: 'POST',
      body: JSON.stringify(body),
    });
    return this.parseSearchResponse(data);
  }

  /**
   * Semantic search using a vector embedding from an LLM.
   */
  async semanticSearch(
    vector: number[],
    filters?: SearchFilters,
    buyerLocation?: Location,
    limit = 20,
  ): Promise<SearchResponse> {
    const body: any = { vector };
    if (filters) body.filters = filters;
    if (buyerLocation) body.buyer_location = buyerLocation;
    body.limit = Math.min(limit, 100);

    const data = await this.request<any>('/search/semantic', {
      method: 'POST',
      body: JSON.stringify(body),
    });
    return this.parseSearchResponse(data);
  }

  /**
   * Get a single listing by ID.
   */
  async getListing(listingId: string, buyerLocation?: Location): Promise<any> {
    const params = new URLSearchParams();
    if (buyerLocation) {
      params.set('buyer_lat', String(buyerLocation.lat));
      params.set('buyer_lon', String(buyerLocation.lon));
    }
    const query = params.toString();
    return this.request<any>(`/listings/${listingId}${query ? '?' + query : ''}`);
  }

  /**
   * Calculate total landed cost for a listing.
   */
  async getTotalCost(listingId: string, buyerLat: number, buyerLon: number, insurance = true): Promise<any> {
    const params = new URLSearchParams({
      buyer_lat: String(buyerLat),
      buyer_lon: String(buyerLon),
      insurance: String(insurance),
    });
    return this.request<any>(`/listings/${listingId}/total-cost?${params}`);
  }

  /**
   * Create an offer on a listing.
   */
  async createOffer(listingId: string, offer: OfferRequest): Promise<Offer> {
    const data = await this.request<any>(`/listings/${listingId}/offers`, {
      method: 'POST',
      body: JSON.stringify(offer),
    });
    return {
      offerId: data.offerId,
      listingId,
      buyerDid: data.buyerDid,
      sellerDid: data.sellerDid,
      offerPrice: data.offerPrice,
      message: data.message,
      status: data.status,
      createdAt: data.createdAt,
      expiresAt: data.expiresAt,
      signature: data.signature,
    };
  }

  /**
   * Respond to an offer (accept, reject, or counter).
   */
  async respondToOffer(
    listingId: string,
    offerId: string,
    response: OfferResponse,
  ): Promise<any> {
    return this.request<any>(`/listings/${listingId}/offers/${offerId}/respond`, {
      method: 'POST',
      body: JSON.stringify(response),
    });
  }

  /**
   * Create an escrow contract.
   */
  async createEscrow(request: EscrowCreateRequest): Promise<Escrow> {
    const data = await this.request<any>('/escrow/create', {
      method: 'POST',
      body: JSON.stringify(request),
    });
    return {
      escrowId: data.escrowId,
      listingId: data.listingId,
      buyerDid: data.buyerDid,
      sellerDid: data.sellerDid,
      status: data.status,
      amounts: data.amounts,
      timeline: data.timeline || [],
      pinCode: data.pinCode,
      inspectionPeriodExpires: data.inspectionPeriodExpires,
      disputeWindowExpires: data.disputeWindowExpires,
    };
  }

  /**
   * Confirm receipt of an escrowed item.
   */
  async confirmEscrow(escrowId: string, pinCode: string, photoEvidence?: Array<{ url: string; type: string }>): Promise<any> {
    const body: any = { pinCode };
    if (photoEvidence) body.photoEvidence = photoEvidence;
    return this.request<any>(`/escrow/${escrowId}/confirm`, {
      method: 'POST',
      body: JSON.stringify(body),
    });
  }

  /**
   * File a dispute for an escrowed transaction.
   */
  async disputeEscrow(
    escrowId: string,
    reason: string,
    description: string,
    photoEvidence?: Array<{ url: string; type: string }>,
  ): Promise<any> {
    const body: any = { reason, description };
    if (photoEvidence) body.photoEvidence = photoEvidence;
    return this.request<any>(`/escrow/${escrowId}/dispute`, {
      method: 'POST',
      body: JSON.stringify(body),
    });
  }

  /**
   * Get trust score for a DID.
   */
  async getTrustScore(did: string): Promise<TrustScore> {
    const data = await this.request<any>(`/trust/${did}`);
    const cs = data.trustScore || {};
    const comp = cs.components || {};
    return {
      overall: cs.overall || 0,
      components: {
        identityVerification: comp.identity_verification || 0,
        transactionCompletion: comp.transaction_completion || 0,
        disputeResolution: comp.dispute_resolution || 0,
        descriptionAccuracy: comp.description_accuracy || 0,
        shippingSpeed: comp.shipping_speed || 0,
      },
      totalTransactions: cs.totalTransactions || 0,
      disputeRate: cs.disputeRate || 0,
      avgResponseTimeMin: cs.avgResponseTimeMin || 0,
      returnRate: cs.returnRate || 0,
      verifiedIdentity: cs.verifiedIdentity || false,
      verifiedSince: cs.verifiedSince || '',
      decay: cs.decay || '',
      categoryExpertise: cs.categoryExpertise || {},
    };
  }

  /**
   * Calculate shipping options.
   */
  async calculateLogistics(request: LogisticsRequest): Promise<LogisticsResponse> {
    return this.request<any>('/logistics/calculate', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  /**
   * Get JSON Schema for a product category.
   */
  async getCategorySchema(categoryId: string): Promise<any> {
    return this.request<any>(`/categories/${categoryId}/schema`);
  }

  /**
   * Bulk fetch listings for indexing.
   */
  async bulkListings(params?: {
    updatedSince?: string;
    categories?: string[];
    cursor?: string;
    limit?: number;
  }): Promise<{ listings: any[]; nextCursor?: string; totalAvailable: number }> {
    const query = new URLSearchParams();
    if (params?.updatedSince) query.set('updated_since', params.updatedSince);
    if (params?.categories) query.set('categories', params.categories.join(','));
    if (params?.cursor) query.set('cursor', params.cursor);
    query.set('limit', String(Math.min(params?.limit || 100, 1000)));
    return this.request<any>(`/listings/bulk?${query}`);
  }

  private parseSearchResponse(data: any): SearchResponse {
    const results = (data.results || []).map((r: any) => ({
      listingId: r.listing_id || r.listingId,
      nodeId: r.node_id || r.nodeId,
      product: {
        category: r.product?.category || '',
        brand: r.product?.brand || '',
        model: r.product?.model || '',
        condition: {
          overallGrade: r.product?.condition?.overall_grade || r.product?.condition?.overallGrade || 'good',
          descriptionAccuracy: r.product?.condition?.description_accuracy || r.product?.condition?.descriptionAccuracy,
        },
      },
      pricing: {
        askPrice: {
          amount: r.pricing?.askPrice?.amount || r.pricing?.ask_price?.amount || 0,
          currency: r.pricing?.askPrice?.currency || r.pricing?.ask_price?.currency || 'RUB',
        },
      },
      totalLandedCost: {
        product: r.total_landed_cost?.product || r.totalLandedCost?.product || 0,
        shipping: r.total_landed_cost?.shipping || r.totalLandedCost?.shipping || 0,
        insurance: r.total_landed_cost?.insurance || r.totalLandedCost?.insurance || 0,
        platformFee: r.total_landed_cost?.platform_fee || r.totalLandedCost?.platformFee || 0,
        total: r.total_landed_cost?.total || r.totalLandedCost?.total || 0,
      },
      seller: {
        did: r.seller?.did || '',
        trustScore: r.seller?.trust_score || r.seller?.trustScore || 0,
      },
      aiConfidence: r.ai_confidence || r.aiConfidence || 0,
    }));

    return {
      results,
      totalEstimated: data.total_estimated || data.totalEstimated || 0,
      nextCursor: data.next_cursor || data.nextCursor,
      searchMetadata: {
        queryUnderstoodAs: data.search_metadata?.query_understood_as || data.search_metadata?.queryUnderstoodAs,
        semanticFallbackUsed: data.search_metadata?.semantic_fallback_used || data.search_metadata?.semanticFallbackUsed || false,
        executionTimeMs: data.search_metadata?.execution_time_ms || data.search_metadata?.executionTimeMs || 0,
      },
    };
  }
}
