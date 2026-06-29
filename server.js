require('dotenv').config();
const express = require('express');
const path = require('path');
const fs = require('fs');
const jwt = require('jsonwebtoken');
const {
  basicFirewall,
  corsPolicy,
  generalLimiter,
  sanitizeRequests,
  securityHeaders
} = require('./backend/middleware/security');

const app = express();
const PORT = process.env.PORT || 3000;
const JWT_SECRET = process.env.JWT_SECRET || 'talentime_academy_jwt_secret_key_2026';
const { db, generateId } = require('./backend/db');
const uploadDir = path.join(__dirname, 'uploads');

// Create uploads directory if it doesn't exist
if (!fs.existsSync(uploadDir)) {
  fs.mkdirSync(uploadDir, { recursive: true });
}

// Middleware
app.set('trust proxy', 1);
app.disable('x-powered-by');
app.use(securityHeaders());
app.use(corsPolicy());
app.use(express.json({ limit: process.env.JSON_BODY_LIMIT || '100kb' }));
app.use(express.urlencoded({ extended: false, limit: process.env.FORM_BODY_LIMIT || '50kb' }));
app.use(sanitizeRequests());
app.use(basicFirewall);
app.use(generalLimiter);

// Helper to parse cookies manually
function getCookie(req, name) {
  const list = {};
  const rc = req.headers.cookie;

  if (rc) {
    rc.split(';').forEach(cookie => {
      const parts = cookie.split('=');
      list[parts.shift().trim()] = decodeURI(parts.join('='));
    });
  }

  return list[name];
}

// Middleware to authenticate static page routes via Cookie
function authenticateStaticRoute(req, res, next) {
  const isCourseRoute = req.path.startsWith('/course') || req.path.startsWith('/list/course');
  
  if (isCourseRoute) {
    const token = getCookie(req, 'token');
    if (!token) {
      return res.redirect(`/customer/login.html?redirect=${encodeURIComponent(req.originalUrl)}`);
    }

    jwt.verify(token, JWT_SECRET, (err, user) => {
      if (err) {
        return res.redirect(`/customer/login.html?redirect=${encodeURIComponent(req.originalUrl)}`);
      }
      req.user = user;
      next();
    });
  } else {
    next();
  }
}

app.use(authenticateStaticRoute);

// Mount API routes
app.use('/api', require('./backend/routes/api'));

// Serve Portal Views
app.get('/dashboard', (req, res) => {
  res.sendFile(path.join(__dirname, 'dashboard', 'index.html'));
});

app.get('/admin', (req, res) => {
  res.sendFile(path.join(__dirname, 'admin-panel', 'index.html'));
});

// Dynamic course detail route
app.get('/course/:id', (req, res, next) => {
  if (req.params.id && req.params.id.length > 5) { // Match Mongo ObjectIDs (typically 24 characters)
    return res.sendFile(path.join(__dirname, 'course', 'detail.html'));
  }
  next();
});

// Serve public static assets
app.use(express.static('.', { extensions: ['html'], dotfiles: 'deny', index: 'index.html', maxAge: '1h' }));
app.use('/uploads', express.static(uploadDir, { dotfiles: 'deny', index: false, maxAge: '1d' }));

// Seed Database (commented out - using Django backend for data)
// seedDatabase();

async function seedDatabase() {
  try {
    const courseCountStmt = db.prepare('SELECT COUNT(*) as count FROM courses');
    const courseCount = courseCountStmt.get().count;
    
    if (courseCount === 0) {
      const courses = [
        {
          id: '65b968600000000000000001',
          name: 'Basic Medical Coding',
          courseCode: 'MED-101',
          description: 'Fundamental training in medical coding principles and documentation standards.',
          category: 'Healthcare BPO',
          level: 'Beginner',
          duration: '90 days',
          eligibility: 'Life Sciences graduates, Medical graduates, general graduates',
          price: 12000,
          instructor: 'Talentime Expert Panel',
          syllabus: 'Anatomy, Medical Terminology, Basic ICD-10-CM guidelines.',
          curriculum: 'Module 1: General ICD-10 Coding Guidelines. Module 2: Medical systems.',
          highlights: JSON.stringify(['Sample Chart and follow up', 'Anatomy & Medical Terminology Foundation', 'Online Mode', '100% Placement Drive']),
          batchTimings: 'Flexible Online',
          placementDetails: 'Full Placement drive assistance with mock diagnostic interviews.',
          certification: 'Certificate of Completion'
        },
        {
          id: '65b968600000000000000002',
          name: 'Masters in Medical Coding Program',
          courseCode: 'MED-202',
          description: 'Specialized professional course developing advanced coding skills for complex medical diagnoses and procedures using ICD-10-CM, CPT, and HCPCS.',
          category: 'Healthcare BPO',
          level: 'Advanced',
          duration: '12 weeks',
          eligibility: 'Basic certified coders or clinical coders',
          price: 18500,
          instructor: 'Senior Coding Expert',
          syllabus: 'Advanced interpreting, complex procedures, specialized systems.',
          curriculum: 'Module 1: Advanced Code Systems. Module 2: Complex Diagnoses.',
          highlights: JSON.stringify(['In-depth industry knowledge', 'Senior coding preparation', 'Real Case Document reviews', 'Career Placement Support']),
          batchTimings: 'Sat-Sun 10AM-12PM IST',
          placementDetails: 'Exclusive hiring runs for clinical coding directors.',
          certification: 'Advanced Certification'
        },
        {
          id: '65b968600000000000000003',
          name: 'Certified Professional Coder (CPC)',
          courseCode: 'MED-303',
          description: 'Globally recognized medical coding program providing comprehensive training in ICD-10-CM, CPT, and HCPCS coding systems.',
          category: 'Healthcare BPO',
          level: 'Professional',
          duration: '90 days',
          eligibility: 'Life sciences graduates or active coding practitioners',
          price: 16000,
          instructor: 'AAPC Certified Trainer',
          syllabus: 'Diagnostic Rules, Code Assignment, Specialty Case Studies.',
          curriculum: 'Module 1: Coding Rules. Module 2: Pathology guidelines. Module 3: AAPC Practice.',
          highlights: JSON.stringify(['AAPC (American Academy of Professional Coders) Cert', 'Coding Accuracy Drills', 'Documentation Best Practices', 'AAPC Exam Support']),
          batchTimings: 'Online',
          placementDetails: 'Admissions team job support network.',
          certification: 'AAPC CPC Certification'
        },
        {
          id: '65b968600000000000000004',
          name: 'Full Stack Developer Program',
          courseCode: 'IT-101',
          description: 'Learn front-end and back-end technologies, databases, APIs, and deployment practices.',
          category: 'IT Software',
          level: 'Beginner to Advanced',
          duration: '12 weeks',
          eligibility: 'Any graduate seeking entry into IT',
          price: 25000,
          instructor: 'Senior Full Stack Engineer',
          syllabus: 'HTML, CSS, JS, Node.js, React, MongoDB',
          curriculum: 'Module 1: Front-end. Module 2: Back-end & Databases. Module 3: Deployment.',
          highlights: JSON.stringify(['Modern technology skills', 'Project-based learning', 'Interview Preparation', 'Direct Hiring Networks']),
          batchTimings: 'Mon-Wed 6PM-8PM IST',
          placementDetails: 'Weekly drive with IT partners.',
          certification: 'Full Stack Developer Certification'
        },
        {
          id: '65b968600000000000000005',
          name: 'Advanced Program in Clinical Research (APCRM)',
          courseCode: 'CLI-101',
          description: 'Comprehensive training covering clinical trials, regulatory requirements, project management, and research operations.',
          category: 'Clinical Research',
          level: 'Professional',
          duration: '10 weeks',
          eligibility: 'Life Sciences graduates',
          price: 22000,
          instructor: 'Clinical Research Director',
          syllabus: 'Clinical trials, regulatory guidelines, drug approval',
          curriculum: 'Module 1: Clinical Trials. Module 2: Regulatory Requirements.',
          highlights: JSON.stringify(['Pharma Regulatory Affairs', 'Clinical Research Associate prep', 'Industry Guidelines', 'Placement Assistance']),
          batchTimings: 'Flexible',
          placementDetails: 'Job support in pharmaceuticals and biotech.',
          certification: 'APCRM Certification'
        },
        {
          id: '65b968600000000000000006',
          name: 'Building Information Modeling (BIM)',
          courseCode: 'ENG-101',
          description: 'Specialized training in MEP, Structural Engineering, and Architectural Modeling.',
          category: 'Engineering',
          level: 'Professional',
          duration: '8 weeks',
          eligibility: 'Engineering Graduates',
          price: 20000,
          instructor: 'Senior BIM Modeler',
          syllabus: 'AutoCAD, Technical Drafting, Design Documentation',
          curriculum: 'Module 1: AutoCAD. Module 2: MEP. Module 3: Structural Modeling.',
          highlights: JSON.stringify(['Industry-focused engineering', 'Technical drafting', 'Design Documentation', 'Placement Support']),
          batchTimings: 'Flexible',
          placementDetails: 'Placement drives for engineering services.',
          certification: 'BIM Certification'
        }
      ];
      
      const insertCourse = db.prepare(`
        INSERT INTO courses (id, name, courseCode, description, category, level, duration, eligibility, price, instructor, syllabus, curriculum, highlights, batchTimings, placementDetails, certification)
        VALUES (@id, @name, @courseCode, @description, @category, @level, @duration, @eligibility, @price, @instructor, @syllabus, @curriculum, @highlights, @batchTimings, @placementDetails, @certification)
      `);
      
      db.transaction((courses) => {
        for (const course of courses) {
          insertCourse.run(course);
        }
      })(courses);
      
      console.log('✓ Seeding complete: 6 courses seeded in SQLite');
    }

    const userCountStmt = db.prepare('SELECT COUNT(*) as count FROM users');
    const userCount = userCountStmt.get().count;
    
    if (userCount === 0) {
      const bcrypt = require('bcrypt');
      const hashedPassword = await bcrypt.hash('Password123', 10);
      
      const seedUsers = [
        {
          id: generateId(),
          firstName: 'Super',
          lastName: 'Admin',
          email: 'talentimebs@gmail.com',
          password: hashedPassword,
          phone: '+91 99999 88888',
          country: 'India',
          role: 'admin',
          status: 'active'
        },
        {
          id: generateId(),
          firstName: 'Meharaj',
          lastName: 'Student',
          email: 'student@talentime.com',
          password: hashedPassword,
          phone: '+91 88888 77777',
          country: 'India',
          role: 'student',
          status: 'active'
        },
        {
          id: generateId(),
          firstName: 'John',
          lastName: 'Trainer',
          email: 'trainer@talentime.com',
          password: hashedPassword,
          phone: '+91 77777 66666',
          country: 'India',
          role: 'trainer',
          status: 'active'
        }
      ];
      
      const insertUser = db.prepare(`
        INSERT INTO users (id, firstName, lastName, email, password, phone, country, role, status)
        VALUES (@id, @firstName, @lastName, @email, @password, @phone, @country, @role, @status)
      `);
      
      db.transaction((users) => {
        for (const user of users) {
          insertUser.run(user);
        }
      })(seedUsers);
      
      console.log('✓ Seeding complete: 3 mock users seeded (Admin, Student, Trainer)');
    }
  } catch (err) {
    console.error('Failed to seed database:', err);
  }
}

// Graceful shutdown
process.on('SIGINT', () => {
  console.log('\\nShutting down server...');
  db.close();
  process.exit(0);
});

app.listen(PORT, () => {
  console.log(`\\nServer running at http://localhost:${PORT}`);
  console.log(`💾 Database: SQLite`);
});
