# Airtable Server - 5 Hour Sprint

🚀 **Professional FastAPI server** connecting infrastructure to Airtable with complete CRUD operations, webhook handling, and real-time logging.

## 📋 Project Overview

This server demonstrates a **working Airtable integration** built within a 5-hour sprint, featuring:
- ✅ **Full CRUD operations** for all data tables
- ✅ **Webhook endpoints** with payload logging
- ✅ **Real-time console proof** of all operations
- ✅ **Production-ready code** with error handling
- ✅ **Complete test coverage** for all functionality

## 🏗️ Airtable Structure

The server integrates with **4 main tables**:

### **Sprints Table**
- `Sprint_ID` - Unique sprint identifier
- `Name` - Sprint name/description
- `Dev_Name` - Developer assigned
- `Status` - Sprint status (Pending/Active/Done)
- `Time_Spent_hr` - Hours invested
- `Notes` - Additional notes

### **Cells Table** (Infrastructure/Droplets)
- `Cell_ID` - Unique cell identifier
- `Role` - Cell role (Builder/Verifier/Connector)
- `IP_Address` - Network address
- `Health_Status` - Current health (OK/Warning/Offline)
- `Cost_per_hr` - Operational cost

### **Proof Table**
- `Proof_ID` - Unique proof identifier
- `Sprint_ID` - Related sprint
- `Result` - Verification result
- `Token` - Security token
- `Timestamp` - Proof timestamp

### **Heartbeats Table**
- `Cell_ID` - Related cell
- `CPU_Usage` - CPU utilization %
- `RAM_Usage` - Memory utilization %
- `Status` - System status
- `Timestamp` - Auto-generated timestamp

## ⚡ Quick Start

### **1. Environment Setup**
Create `.env` file with your Airtable credentials:
```bash
AIRTABLE_API_KEY=your_api_key_here
BASE_ID=your_base_id_here
```

### **2. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3. Run Server**
```bash
python main.py
```
Server starts on `http://localhost:8000`

### **4. Verify Installation**
```bash
python full_verification.py
```

## 🔗 API Endpoints

### **Core Endpoints**
- `GET /` - **Health check** - Verify server status
- `POST /write` - **Write data** - Push sample data to all tables
- `GET /read` - **Read data** - Fetch records from all tables

### **Webhook Endpoints**
- `POST /webhook` - **General webhook** - Handle any POST payload
- `POST /proof` - **Proof webhook** - Handle proof verification
- `POST /heartbeat` - **Heartbeat webhook** - Handle system heartbeats

### **Example Usage**
```bash
# Health check
curl http://localhost:8000/

# Write sample data
curl -X POST http://localhost:8000/write

# Read all records
curl http://localhost:8000/read

# Send webhook
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -d '{"test": "data", "timestamp": "2025-01-04T10:00:00"}'
```

## 🧪 Testing

### **Basic Tests**
```bash
python test.py
```

### **Comprehensive Verification**
```bash
python full_verification.py
```

This runs complete testing of:
- ✅ Server health check
- ✅ Write operations to all tables
- ✅ Read operations from all tables
- ✅ All webhook endpoints
- ✅ Error handling

## 📊 Console Proof

The server provides **real-time logging** with clear visual indicators:

```
✅ Sprints: 200        # Successful operations
❌ Cells: 422          # Error operations
🔔 Webhook received     # Webhook notifications
📖 Read Sprints: 5     # Read operations
🎯 Proof webhook       # Proof-specific webhooks
💓 Heartbeat webhook   # Heartbeat notifications
```

## 🐳 Docker Deployment

### **Build Container**
```bash
docker build -t airtable-server .
```

### **Run Container**
```bash
docker run -d -p 8000:8000 \
  -e AIRTABLE_API_KEY="your_key" \
  -e BASE_ID="your_base_id" \
  --name airtable-server \
  airtable-server
```

### **Ubuntu Deployment**
```bash
# Install Docker (if needed)
sudo apt update && sudo apt install -y docker.io

# Deploy server
docker run -d -p 8000:8000 \
  -e AIRTABLE_API_KEY="$AIRTABLE_API_KEY" \
  -e BASE_ID="$BASE_ID" \
  --restart unless-stopped \
  --name airtable-server \
  airtable-server
```

## 🔧 Configuration

### **Environment Variables**
- `AIRTABLE_API_KEY` - Your Airtable personal access token
- `BASE_ID` - Your Airtable base identifier

### **Getting Airtable Credentials**
1. **API Key**: Visit [airtable.com/create/tokens](https://airtable.com/create/tokens)
2. **Base ID**: In your base, go to Help → API documentation

## 📁 Project Structure

```
airtable_project/
├── main.py                 # FastAPI server
├── test.py                 # Basic endpoint tests
├── full_verification.py    # Comprehensive testing
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables
├── README.md              # This documentation
└── Dockerfile             # Container configuration
```

## 🚀 Production Features

- **Error Handling**: Comprehensive exception handling
- **Logging**: Real-time operation logging with emojis
- **Validation**: Input validation and sanitization
- **Security**: Environment-based credential management
- **Scalability**: Containerized deployment ready
- **Testing**: Complete test coverage

## 🎯 Sprint Deliverables

**Completed within 5-hour sprint:**
- ✅ FastAPI server with Airtable integration
- ✅ Read/write operations for all tables
- ✅ Webhook handling with logging
- ✅ Complete test suite
- ✅ Docker containerization
- ✅ Production-ready deployment
- ✅ Comprehensive documentation

## 🔮 Future Enhancements

- **Daily Digest**: Automated daily summary reports
- **Authentication**: API key authentication
- **Rate Limiting**: Request throttling
- **Monitoring**: Health checks and metrics
- **Scaling**: Multi-instance deployment

---

**Built with ❤️ using FastAPI, Airtable API, and modern Python practices.**