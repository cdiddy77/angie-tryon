# Product Requirements Document: Angie-Tryon

## 1. Executive Summary

Angie-Tryon is a mobile-first web application that enables users to create photo-realistic images of themselves wearing different clothing combinations using generative AI models. Built on the Boards framework, it provides an intuitive interface for virtual try-on experiences, allowing users to mix and match clothing items from their personal wardrobe collection.

### Key Features
- Virtual try-on using AI-powered image generation
- Personal wardrobe management with automatic categorization
- SMS-based authentication for frictionless access
- Social sharing of generated outfit visualizations
- Mobile-optimized interface with native camera integration

## 2. Product Vision & Objectives

### Vision Statement
Create the most intuitive and accessible virtual wardrobe application that empowers users to visualize outfit combinations before purchasing or wearing them.

### Primary Objectives
1. **Reduce decision fatigue** in daily outfit selection
2. **Enable virtual try-before-buy** for online shopping scenarios
3. **Create shareable fashion content** for social validation
4. **Build personal style catalogs** for wardrobe organization

### Success Metrics
- User engagement: Daily active users creating at least one outfit
- Generation quality: User satisfaction with outfit realism
- Sharing rate: Percentage of generations shared socially
- Retention: Weekly returning users

## 3. User Personas

### Primary Persona: Fashion-Conscious Mobile User
- **Demographics**: 18-35 years old, smartphone-first
- **Behavior**: Takes screenshots while shopping online, seeks social validation for outfit choices
- **Pain Points**: Uncertainty about how clothes will look on them, difficulty visualizing outfit combinations
- **Goals**: Make confident fashion choices, organize wardrobe digitally

### Secondary Persona: Online Shopper
- **Demographics**: 25-45 years old, frequent e-commerce user
- **Behavior**: Screenshots items from shopping apps, compares multiple options
- **Pain Points**: High return rates due to fit/style mismatches
- **Goals**: Reduce purchase regret, visualize items before buying

## 4. User Stories

### Authentication & Onboarding
- As a new user, I want to sign up using only my phone number so I can start using the app immediately
- As a returning user, I want the app to remember my selections so I don't have to reconfigure each time

### Wardrobe Management
- As a user, I want to add clothing items from my clipboard so I can quickly save items I find online
- As a user, I want to photograph my existing clothes so I can digitize my wardrobe
- As a user, I want to upload multiple photos of myself so I can try outfits on different poses

### Outfit Creation
- As a user, I want to select items for each clothing slot so I can build complete outfits
- As a user, I want to see my selections update in real-time so I know what I've chosen
- As a user, I want to generate a realistic visualization so I can see how the outfit looks

### Sharing & Management
- As a user, I want to share generated outfits so I can get feedback from friends
- As a user, I want to save successful combinations so I can reference them later
- As a user, I want to regenerate outfits with variations so I can explore alternatives

## 5. Functional Requirements

### 5.1 Authentication System
- **SMS Magic Link Authentication**
  - No traditional login/password screens
  - Phone number verification via SMS
  - Automatic session persistence
  - Integration with Supabase Auth

### 5.2 Board & Storage System
- **Single Board Per User**
  - All wardrobe items stored in one board
  - Automatic creation on first use
  - Private visibility by default

- **Tagging System**
  - Many-to-many relationship between generations and tags
  - Automatic tagging on upload based on slot selection
  - Supported tags: "model", "top", "bottom", "shoes", "socks", "hat", "outfit"
  - Filter and search by tags

### 5.3 Image Input Methods
- **Clipboard Paste**
  - Direct paste into text input field
  - Automatic image detection and extraction
  - Support for screenshots from any app

- **Camera Capture**
  - Native browser camera API
  - Direct capture to wardrobe
  - Automatic background removal option

- **Photo Library Upload**
  - Multiple file selection
  - Drag and drop support (desktop)
  - File picker (mobile)

### 5.4 Outfit Slots
- **Model Slot**
  - User's photo (multiple supported)
  - Tagged as "model"
  - Remembers last selection

- **Clothing Slots**
  - Inside Top (base layer)
  - Outside Top (jacket/outer)
  - Bottoms (pants/skirts/dresses)
  - Shoes
  - Socks (optional)
  - Hat (optional)

### 5.5 Generation Process
- **Pre-generation State**
  - Display all slots with selections
  - "Add an item" prompts for empty slots
  - Visual indicators for selected items
  - "Generate Outfit" CTA button

- **Generation Execution**
  - Progress indicator during processing
  - Estimated time display (15-30 seconds)
  - Queued via Boards worker system

- **Post-generation State**
  - Full-screen result display
  - Share and download options
  - Regenerate capability
  - Return to selection state

### 5.6 Selection Interface
- **Drawer Component**
  - Slides up from bottom (mobile)
  - Modal overlay (desktop)
  - Grid view of available items
  - Input methods at top (Camera, Photos, Paste)
  - "See All" link for full collection view

### 5.7 Sharing Features
- **Browser Platform Share API**
  - Native sharing sheet on mobile
  - Fallback to URL copy on desktop
  - Include generated image

- **Download Option**
  - Save generated image locally
  - Original resolution preservation

### 5.8 State Management
- **Local Storage**
  - Remember last selections per slot
  - Persist user preferences
  - Cache recently used items

- **Session State**
  - Current outfit configuration
  - Generation progress
  - Error recovery

## 6. Technical Architecture

### 6.1 Frontend Stack
- **Framework**: Next.js 14 (App Router)
- **UI Library**: Shadcn/ui
- **Styling**: Tailwind CSS
- **State**: React hooks + local storage
- **API Client**: @weirdfingers/boards hooks

### 6.2 Backend Services
- **API Server**: Boards GraphQL API
- **Worker**: Dramatiq job processor
- **Database**: PostgreSQL (via Supabase)
- **Storage**: Supabase Storage
- **Cache**: Redis

### 6.3 AI/ML Services
- **Virtual Try-On**: fal-ai/kling/v1-5/kolors-virtual-try-on
- **Background Removal**: fal-ai/bria/background/remove
- **Image Processing**: Boards generation pipeline

### 6.4 Authentication
- **Provider**: Supabase Auth
- **Method**: SMS OTP (One-Time Password)
- **Session**: JWT tokens
- **Persistence**: Secure HTTP-only cookies

### 6.5 Data Model

```typescript
// Generation with Tags (existing Boards model extended)
interface Generation {
  id: string;
  boardId: string;
  userId: string;
  artifactUrl: string;
  tags: Tag[];
  metadata: {
    slot?: 'model' | 'top' | 'bottom' | 'shoes' | 'socks' | 'hat';
    isOutfit?: boolean;
  };
  createdAt: Date;
}

// Tag (new many-to-many relationship)
interface Tag {
  id: string;
  name: string;
  generations: Generation[];
}

// User Preferences (local storage)
interface UserPreferences {
  lastSelections: {
    model?: string;
    insideTop?: string;
    outsideTop?: string;
    bottom?: string;
    shoes?: string;
    socks?: string;
    hat?: string;
  };
  settings: {
    autoRemoveBackground?: boolean;
  };
}
```

## 7. Non-Functional Requirements

### 7.1 Performance
- Generation time: 15-30 seconds typical
- Page load: < 2 seconds on 4G
- Image upload: Progress indication required
- Responsive UI: 60fps scrolling and interactions

### 7.2 Scalability
- Support unlimited items per user
- No hard limits on generation count
- Horizontal scaling via worker instances

### 7.3 Security
- All data encrypted in transit (HTTPS)
- User isolation at database level
- Sanitized user inputs
- Rate limiting on generation requests

### 7.4 Accessibility
- WCAG 2.1 AA compliance
- Keyboard navigation support
- Screen reader compatibility
- High contrast mode support

### 7.5 Browser Support
- Chrome/Edge (latest 2 versions)
- Safari iOS (latest 2 versions)
- Firefox (latest 2 versions)
- Progressive enhancement for older browsers

## 8. Design Constraints

### 8.1 Mobile-First
- Touch-optimized interactions
- Thumb-reachable CTAs
- Portrait orientation primary
- Native mobile APIs (camera, share)

### 8.2 Image Requirements
- Portrait orientation only
- Automatic resizing for uploads
- WebP with fallbacks
- Lazy loading for collections

### 8.3 Platform Limitations
- Clipboard API varies by browser
- Share API requires HTTPS
- Camera access requires permissions

## 9. Dependencies

### 9.1 External Services
- Supabase (auth, database, storage)
- fal.ai (image generation)
- SMS provider (via Supabase)

### 9.2 Internal Packages
- @weirdfingers/boards (core functionality)
- @weirdfingers/boards-auth-supabase (auth adapter)

### 9.3 Third-Party Libraries
- Shadcn/ui components
- Tailwind CSS
- Next.js framework

## 10. Release Strategy

### 10.1 MVP Scope (Version 1.0)
- ✅ SMS authentication
- ✅ Basic wardrobe management
- ✅ 6 outfit slots
- ✅ Image generation
- ✅ Social sharing
- ✅ Background removal
- ✅ Multiple models per user
- ✅ Local storage persistence

### 10.2 Future Enhancements (Version 2.0)
- ⏳ E-commerce integration (URL scraping)
- ⏳ Automatic metadata extraction
- ⏳ Wardrobe organization tools
- ⏳ Outfit history and favorites
- ⏳ Style recommendations
- ⏳ Social features (public profiles)
- ⏳ Advanced editing tools

### 10.3 Potential Features (Version 3.0)
- ⏳ AI style advisor
- ⏳ Weather-based suggestions
- ⏳ Wardrobe analytics
- ⏳ Collaborative styling
- ⏳ Brand partnerships

## 11. Open Design Decisions

### 11.1 Generation Implementation
**Status**: Unresolved - Separate ticket required

The exact implementation of the outfit generation process needs further investigation:
- How to composite multiple clothing items onto the model
- Handling of layering (inside vs outside top)
- Pose matching between model and clothing
- Background preservation vs generation
- Quality vs speed tradeoffs

### 11.2 Tagging Granularity
Consider whether tags need subcategories:
- "top" → "top:shirt", "top:jacket", "top:sweater"
- Automatic vs manual categorization
- User-defined tags

### 11.3 Credit System
Determine if generation costs need management:
- Free tier limitations
- Credit purchase options
- Optimization strategies

## 12. Success Criteria

### 12.1 Launch Metrics
- Successful authentication flow
- Complete outfit generation pipeline
- Stable image upload/storage
- Functional sharing mechanism

### 12.2 Quality Metrics
- Generation success rate > 95%
- User satisfaction > 4/5 stars
- Page load time < 2 seconds
- Zero data loss incidents

### 12.3 Adoption Metrics
- 100 active users in first month
- 50% weekly retention rate
- 10% social sharing rate
- 5+ items per user wardrobe

## Appendix A: Technical Specifications

### API Endpoints (GraphQL)
- `createBoard`: Initialize user wardrobe
- `uploadArtifact`: Add wardrobe items
- `tagGeneration`: Apply tags to items
- `getGenerationsByTag`: Filter wardrobe
- `createGeneration`: Trigger outfit creation

### Storage Structure
```
/users/{userId}/
  /wardrobe/
    /items/{generationId}
  /outfits/{generationId}
```

### Environment Variables
```
NEXT_PUBLIC_SUPABASE_URL
NEXT_PUBLIC_SUPABASE_ANON_KEY
NEXT_PUBLIC_BOARDS_API_URL
FAL_KEY
```

## Appendix B: References

- Mockups: `/design/angie-tryon/*.png`
- Template Repository: https://github.com/cdiddy77/friends-and-family-supabase
- Boards Documentation: `/apps/docs/`
- fal.ai Model Docs: https://fal.ai/models