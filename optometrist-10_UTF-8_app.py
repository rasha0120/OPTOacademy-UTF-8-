# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd

# ================== إعداد الصفحة ==================
st.set_page_config(page_title="OptoAcademy - Dashboard", layout="wide", page_icon="🎓")

# دعم الكتابة من اليمين لليسار (RTL)
st.markdown("""
<style>
    .stApp { direction: rtl; }
    [data-testid="stMarkdownContainer"] { direction: rtl; text-align: right; }
    h1, h2, h3, h4, p, li { text-align: right; }
    table { direction: rtl; text-align: right; }
    [data-testid="stSidebar"] { direction: rtl; text-align: right; }
</style>
""", unsafe_allow_html=True)

# ================== دوال مساعدة ==================
def interactive_case(key, title, scenario, question, options, correct_index, explanation):
    """عرض حالة مرضية تفاعلية مع تحقق من الإجابة"""
    st.subheader(title)
    st.info(scenario)
    answer = st.radio(f"❓ {question}", options, key=f"{key}_q")
    if st.button("🔍 تحقق من الإجابة", key=f"{key}_btn"):
        if options.index(answer) == correct_index:
            st.success(f"✅ إجابة صحيحة! {explanation}")
        else:
            st.error(f"❌ ليست الإجابة الأنسب. {explanation}")

# ================== الهيدر ==================
st.markdown("""
    <div style="background-color: #1E3A8A; padding: 20px; border-radius: 10px; text-align: center; color: white;">
        <h1>🎓 OptoAcademy Clinical Dashboard</h1>
        <h3>دليل الحلول البصرية والقياسات المعيارية لسلامة المرضى</h3>
        <p><b>إعداد وتقديم: Optometrist / Rasha Hassan</b></p>
    </div>
""", unsafe_allow_html=True)

st.write("")

# ================== القائمة الجانبية ==================
st.sidebar.title("📌 الأقسام الإكلينيكية")
section = st.sidebar.radio("اختر القسم:", [
    "1. الأخطاء الانكسارية وازدواجية الرؤية (Refraction & BV)",
    "2. العدسات اللاصقة والقرنية (Contact Lenses & Cornea)",
    "3. المياه الزرقاء وضغط العين (Glaucoma & IOP)",
    "4. بصريات الأطفال وتدريب البصر (Pediatrics & VT)",
    "5. الملخص الإكلينيكي الشامل (Clinical Summary)"
])

# =========================================================
# القسم الأول: الانكسار والرؤية ثنائية العين
# =========================================================
if "1." in section:
    st.header("👓 1. الأخطاء الانكسارية وإدارة الرؤية ثنائية العين")

    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 خطة الحلول البصرية", "🛡️ قياسات السلامة",
        "🩺 حالة تفاعلية", "🧮 حاسبة Vertex Distance"])

    with tab1:
        st.subheader("دليل خطوات الفحص والانكسار الدقيق")
        st.markdown("""
        1. **الفحص المبدئي (Objective Refraction):** إجراء Retinoscopy أو Autorefractor لتحديد الخطأ الانكساري الأولي.
        2. **الفحص الذاتي (Subjective Refraction):** تحديد أقصى قوة زائدة لتحقيق أفضل حدة أبصار (MPMVA).
        3. **تضبيط الاستجماتيزم (Jackson Cross-Cylinder):** تحديد المحور (Axis) بدقة ثم القوة (Power).
        4. **التوازن بين العينين (Binocular Balancing):** استخدام تقنية Alternating Cover Test أو Prism Dissociation لضمان استرخاء التكيف بالعينين.
        5. **تقييم الرؤية القريبة (Near Add):** تحديد الاحتياج للقراءة بناءً على عمر المريض ومسافة العمل.
        """)

    with tab2:
        st.subheader("أهم قياسات السلامة لضمان راحة المريض")
        df_safety1 = pd.DataFrame({
            "المعيار / القياس": ["مسافة المدى البؤري (Vertex Distance)", "مسافة حدقة العين (PD)", "Binocular Balance"],
            "القيمة الطبيعية / الهدف": ["12mm - 14mm", "دقيقة لكل عين (Monocular PD)", "تكافؤ التكيف بين العينين"],
            "مخاطر التجاهل": ["تغير قوة العدسة في الدرجات العالية (>4.00D)",
                              "إجهاد بصري ورؤية مزدوجة ناتجة عن منشور غير مقصود",
                              "إجهاد وصداع مستمر"]
        })
        st.table(df_safety1)

    with tab3:
        interactive_case(
            key="case1",
            title="حالة تفاعلية: High Myopia with Astigmatism & Asthenopia",
            scenario="""
            **المريض:** شاب بعمر 24 سنة، يشكو من صداع وإجهاد عند ارتداء نظارته الجديدة.
            **القياسات الحالية:**
            * OD: -6.50 / -1.50 x 180
            * OS: -6.00 / -1.25 x 175
            **معطيات إضافية:** النظارة القديمة VD = 12mm، والإطار الجديد VD = 15mm مع خطأ 3mm في الـ PD.
            **السؤال:** ما هو السبب الأكثر ترجيحاً للأعراض؟
            """,
            question="ما السبب الأرجح لصداع المريض مع النظارة الجديدة؟",
            options=["خلل في تصنيع العدسات (Wavefront Error)",
                     "تغيّر الـ Vertex Distance مع خطأ في الـ PD دون تعديل القوة",
                     "زيادة التصحيح القريبي بشكل مفرط"],
            correct_index=1,
            explanation="زيادة مسافة الـ VD من 12 إلى 15mm مع قوى عالية (>4.00D)، تُغيّر القوة الفعالة عند القرنية، وإضافة خطأ الـ PD يولّد منشوراً غير مقصود (Induced Prism). الحل: إعادة حساب القوة + ضبط Monocular PD."
        )

    with tab4:
        st.subheader("🧮 حاسبة تعديل القوة حسب Vertex Distance")
        st.caption("المعادلة: F₂ = F₁ ÷ (1 + F₁ × Δv) — تُستخدم للقوى فوق ±4.00D")
        col1, col2 = st.columns(2)
        with col1:
            old_power = st.number_input("قوة العدسة الحالية (D):", value=-6.50, step=0.25, key="vp")
            old_vd = st.number_input("مسافة VD الأصلية (mm):", value=12, step=1, key="v1")
            new_vd = st.number_input("مسافة VD الجديدة (mm):", value=15, step=1, key="v2")
        with col2:
            if old_power != 0:
                delta_v = (new_vd - old_vd) / 1000  # تحويل للمتر
                new_power = old_power / (1 + old_power * delta_v)
                rounded = round(new_power * 4) / 4  # تقريب لأقرب 0.25
                st.metric("القوة الجديدة المطلوبة (دقيقة):", f"{new_power:+.2f} D")
                st.metric("القوة بعد التقريب الإكلينيكي (0.25D):", f"{rounded:+.2f} D")
                st.caption(f"التغير المطلوب: {new_power - old_power:+.2f} D")
            else:
                st.warning("أدخل قوة عدسة صحيحة")

# =========================================================
# القسم الثاني: العدسات اللاصقة والقرنية
# =========================================================
elif "2." in section:
    st.header("👁️ 2. العدسات اللاصقة وفحوصات القرنية")

    tab1, tab2, tab3 = st.tabs(["📋 خطة الملاءمة (Fitting Protocol)", "🛡️ قياسات السلامة", "🩺 حالة تفاعلية"])

    with tab1:
        st.subheader("خطوات ملاءمة العدسات اللاصقة الصلبة/الخاصة (RGP / Scleral)")
        st.markdown("""
        1. **قياسات القرنية (Topography / Keratometry):** تحديد قيم K1, K2 ونمط انحناء القرنية.
        2. **اختيار عدسة التجربة (Trial Lens):** اختيار Base Curve بناءً على متوسط Flat K.
        3. **تقييم الصبغة (Fluorescein Pattern Analysis):** فحص نمط الفلوريسين تحت الضوء الأزرق (Cobalt Blue).
        4. **الانكسار الإضافي (Over-Refraction):** إجراء Sphero-cylindrical Over-Refraction للحصول على حدة أبصار 6/6.
        5. **تقييم الحواف والحركة (Edge Clearance & Movement):** التأكد من حركة العدسة بمقدار 1.0 - 1.5 ملم مع الرمش.
        """)

    with tab2:
        st.subheader("قياسات السلامة لحماية القرنية من الخلل النسيجي")
        df_safety2 = pd.DataFrame({
            "الفحص": ["زمن تكسر الفيلم الدمعي (TBUT)", "نفاذية الأكسجين (Dk/t)", "Fluorescein Staining"],
            "الحد الآمن": ["> 10 ثوانٍ", "> 125 للنوم / > 24 للارتداء اليومي", "Grade 0 - Grade 1 max"],
            "المخاطر الإكلينيكية": ["جفاف حاد وعدم تحمل العدسة",
                                    "نقص أكسجة القرنية (Neovascularization)",
                                    "تقرحات وقرح القرنية جرثومية"]
        })
        st.table(df_safety2)

    with tab3:
        interactive_case(
            key="case2",
            title="حالة تفاعلية: Keratoconus (القرنية المخروطية)",
            scenario="""
            **المشكلة:** مريض 28 سنة يعاني من انخفاض حدة الأبصار بالنظارة (6/18) مع استجماتيزم غير منتظم.
            **التشخيص:** قرنية مخروطية متوسطة Stage II.
            **السؤال:** ما الحل البصري الأنسب لتحقيق حدة أبصار أفضل؟
            """,
            question="ما الخيار البصري الأمثل لهذا المريض؟",
            options=["تحديث النظارة بقوى أعلى",
                     "عدسات لاصقة طرية Toric عادية",
                     "عدسات صلبة نافذة للغازات (RGP) أو Scleral"],
            correct_index=2,
            explanation="العدسات الصلبة تُنشئ سطحاً انكسارياً كروياً منتظماً فوق القرنية غير المنتظمة، فتعوّض الاستجماتيزم غير المنتظم الذي لا تستطيع النظارة ولا العدسات الطرية تصحيحه. معيار السلامة: ضمان Apical Clearance لتجنب تندب قمة المخروط."
        )

# =========================================================
# القسم الثالث: الجلوكوما وضغط العين
# =========================================================
elif "3." in section:
    st.header("🩺 3. المياه الزرقاء وفحوصات ضغط العين (Glaucoma & IOP)")

    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 بروتوكول التشخيص", "🛡️ قياسات السلامة",
        "🩺 حالة تفاعلية", "🧮 حاسبة تصحيح IOP"])

    with tab1:
        st.subheader("خطوات المسح والتقييم لمرضى الجلوكوما")
        st.markdown("""
        1. **قياس ضغط العين (IOP Measurement):** باستخدام Goldmann Applanation Tonometry (GAT).
        2. **قياس سمك القرنية (Pachymetry - CCT):** لتعديل قراءة ضغط العين الحقيقية.
        3. **تقييم زاوية الغرفة الأمامية (Van Herick / Gonioscopy):** لضمان عدم إغلاق الزاوية.
        4. **فحص العصب البصري (Optic Disc Assessment):** تقييم C/D Ratio ومتابعة Neuroretinal Rim.
        5. **فحص المجال البصري و OCT:** إجراء Visual Field Test و RNFL OCT لتقييم التلف الوظيفي والتركيبي.
        """)

    with tab2:
        st.subheader("معايير السلامة عند قياس ضغط العين")
        df_safety3 = pd.DataFrame({
            "المعيار": ["تعقيم رأس الجهاز (GAT Tip)", "سمك القرنية المركزي (CCT)", "عمق الغرفة الأمامية"],
            "القيمة / الإجراء": ["تطهير بـ Alcohol 70% أو مسحات معقمة", "المتوسط ~545 microns", "Grade 3 إلى Grade 4 (Van Herick)"],
            "الهدف من السلامة": ["منع انتقال العدوى الفيروسية (مثل Adenovirus)",
                                 "تجنب التقدير الخاطئ لضغط العين (Over/Underestimation)",
                                 "تجنب حدوث إغلاق مفاجئ للزاوية (Acute Angle Closure)"]
        })
        st.table(df_safety3)

    with tab3:
        interactive_case(
            key="case3",
            title="حالة تفاعلية: Ocular Hypertension vs Normal Tension Glaucoma",
            scenario="""
            **المريض:** حالة 52 سنة، قراءة ضغط العين GAT = 24 mmHg.
            **القياسات المفصلة:** سمك القرنية CCT = 590 microns (قرنية سميكة).
            **السؤال:** ما الإجراء الإكلينيكي الصحيح؟
            """,
            question="ما القرار الأنسب بناءً على القياسات؟",
            options=["بدء أدوية خفض الضغط فوراً لأن القراءة مرتفعة",
                     "تصحيح القراءة بناءً على سمك القرنية أولاً — الضغط الحقيقي أقل من المقروء",
                     "إجراء Laser Iridotomy وقائي"],
            correct_index=1,
            explanation="القرنية السميكة (590µm > 545µm) تجعل GAT يُبالغ في قراءة الضغط. التصحيح وفق سمك القرنية يُظهر ضغطاً حقيقياً ضمن الحدود الطبيعية تقريباً، مما يمنع علاجاً دوائياً غير مبرر — مع ضرورة المتابعة الدورية للعصب البصري والمجال."
        )

    with tab4:
        st.subheader("🧮 حاسبة تصحيح IOP حسب سمك القرنية")
        st.caption("تقدير تقريبي: ~2.5 mmHg لكل 50µm انحرافاً عن المعيار (545µm)")
        col1, col2 = st.columns(2)
        with col1:
            cct = st.number_input("سمك القرنية CCT (microns):", value=545, step=1, key="cct")
            iop_measured = st.number_input("قراءة GAT المقاسة (mmHg):", value=20.0, step=0.5, key="iop")
        with col2:
            correction = (cct - 545) * 2.5 / 50
            corrected_iop = iop_measured - correction
            st.metric("قيمة التصحيح:", f"{correction:+.2f} mmHg")
            st.metric("الضغط المقدَّر المعدَّل:", f"{corrected_iop:.1f} mmHg")

            if corrected_iop > 21:
                st.error("⚠️ أعلى من الحد الطبيعي — يلزم تقييم شامل (Disc + VF + OCT)")
            else:
                st.success("✅ ضمن الحدود الطبيعية تقريباً")
        st.caption("⚠️ ملاحظة: نماذج التصحيح تختلف بين الدراسات (Ehlers، Doughty-Zaman). القيم تعليمية تقريبية ولا تُغني عن الحكم الإكلينيكي.")

# =========================================================
# القسم الرابع: بصريات الأطفال
# =========================================================
elif "4." in section:
    st.header("👶 4. بصريات الأطفال وتدريب البصر (Pediatrics & VT)")

    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 بروتوكول التشخيص والعلاج", "🛡️ قياسات السلامة",
        "🩺 حالة تفاعلية", "🧮 حاسبة ساعات التغطية"])

    with tab1:
        st.subheader("خطوات التعامل مع كسل العين والانحراف (Amblyopia & Strabismus)")
        st.markdown("""
        1. **الانكسار الشامل تحت الشلل التكيفي (Cycloplegic Refraction):** استخدام قطرات شلل التكيف لتحديد الخطأ الانكساري الحقيقي.
        2. **تقييم انحراف العين (Cover Test & Hirschberg):** تحديد نوع ودرجة الحول (Tropia vs Phoria).
        3. **الوصفة النظارية الكاملة (Full Optical Correction):** إعطاء التصحيح الانكساري الكامل لعدة أسابيع قبل التغطية.
        4. **علاج التغطية / التغبيش (Patching / Penalization Protocol):** تحديد عدد الساعات بناءً على درجة الكسل.
        5. **تمارين تدريب البصر (Vision Therapy):** تمارين التجميع والاندماج (Convergence & Accommodation Exercises).
        """)

    with tab2:
        st.subheader("قياسات السلامة الخاصة بالأطفال")
        df_safety4 = pd.DataFrame({
            "المجال": ["قطرات الشلل التكيفي (Cycloplegics)", "تغطية العين (Patching)", "إطار النظارة (Frame Safety)"],
            "الإجراء الآمن": ["استخدام Cyclopentolate 0.5% - 1% والضغط على المجرى الدمعي",
                              "التأكد من تغطية العين السليمة فقط ولعدد ساعات محدد",
                              "إطارات سيليكون خالية من المعادن مع عدسات Polycarbonate"],
            "مخاطر الخلل": ["سمية جهازيّة وزيادة ضربات القلب لدى الأطفال",
                            "حدوث كسل عكسي (Occlusion Amblyopia) في العين السليمة",
                            "كسر العدسات وإصابة العين أثناء اللعب"]
        })
        st.table(df_safety4)

    with tab3:
        interactive_case(
            key="case4",
            title="حالة تفاعلية: Anisometropic Amblyopia (كسل العين التبايني)",
            scenario="""
            **المريض:** طفل بعمر 6 سنوات.
            **الفحص:** OD: +1.00DS (6/6) | OS: +4.50DS (6/24).
            **السؤال:** ما الخطوة العلاجية الأولى الصحيحة؟
            """,
            question="ما الإجراء الأول في خطة العلاج؟",
            options=["البدء بتغطية العين السليمة (OD) فوراً قبل أي شيء آخر",
                     "وصف النظارة الكاملة أولاً مع فترة تكيف 6-8 أسابيع قبل التغطية",
                     "التحويل الجراحي الفوري لضبط العضلات"],
            correct_index=1,
            explanation="يجب إعطاء التصحيح الانكساري الكامل أولاً — وحده قد يحسّن الحدة، وفق بروتوكولات PEDIG، في حالات كثيرة. بعدها تبدأ التغطية (2-4 ساعات يومياً) مع متابعة كل 4-6 أسابيع لتفادي Occlusion Amblyopia."
        )

    with tab4:
        st.subheader("🧮 حاسبة ساعات التغطية الموصى بها (وفق PEDIG)")
        col1, col2 = st.columns(2)
        with col1:
            severity = st.selectbox("درجة كسل العين:", [
                "خفيف - متوسط (20/40 - 20/80)",
                "شديد (20/100 - 20/400)"])
        with col2:
            if "خفيف" in severity:
                st.metric("ساعات التغطية اليومية", "2 - 3 ساعات")
                st.caption("مع أنشطة قريبة دقيقة (رسم، قراءة، ألغاز)")
            else:
                st.metric("ساعات التغطية اليومية", "6 ساعات")
                st.caption("مع مراقبة العين السليمة كل 4-6 أسابيع")
        st.caption("⚠️ دائماً: التصحيح النظاري الكامل أولاً، والمتابعة الدورية إلزامية لتفادي كسل التغطية العكسي.")

# =========================================================
# القسم الخامس: الملخص الإكلينيكي الشامل
# =========================================================
if "5." in section:
    st.header("📚 الملخص الإكلينيكي الشامل (Clinical Summary)")

    st.subheader("أولاً: خطط الحلول البصرية (Protocols)")
    st.markdown("""
    * **الانكسار:** التدرج المنهجي من الفحص الموضوعي (Retinoscopy) إلى الفحص الذاتي والتوازن البصري بين العينين لضمان دقة الوصفة.
    * **العدسات اللاصقة:** الاعتماد على خرائط القرنية (Topography) لملاءمة العدسات الصلبة وتقييم الفلوريسين والسكليرال.
    * **الجلوكوما:** دمج قياسات الضغط (GAT) مع سمك القرنية المركزي (CCT) وفحص المجال البصري و OCT.
    * **الأطفال:** الانكسار بعد الشلل التكيفي (Cycloplegic Refraction) والتصحيح الكامل قبل بروتوكولات التغطية.
    """)

    st.subheader("ثانياً: جدول قياسات السلامة المتقاطعة")
    df_summary = pd.DataFrame({
        "القسم": ["Refraction", "Contact Lenses", "Glaucoma", "Pediatrics"],
        "القياس الإكلينيكي": ["Vertex Distance (VD)", "Tear Break-Up Time (TBUT)",
                              "Central Corneal Thickness (CCT)", "Lens Material"],
        "المعيار الآمن": ["12 - 14 mm", "> 10 seconds", "545 µm (Standard)", "Polycarbonate / Trivex"],
        "المخاطر عند التجاهل": ["خطأ في القوة للدرجات العالية (>4.00D)",
                                "جفاف حاد وتقرحات قرنية",
                                "خطأ في قراءة IOP",
                                "كسر العدسات وإصابات العين"]
    })
    st.table(df_summary)

    st.subheader("ثالثاً: الحالات المرضية المدمجة")
    st.markdown("""
    * **High Myopia & VD Error:** تصحيح إجهاد نتيجة تغافل الـ VD والـ Monocular PD.
    * **Keratoconus RGP Fitting:** حدة 6/6 بعدسات صلبة مع الحفاظ على سلامة القمة.
    * **Pachymetry Adjusted IOP:** تجنب علاج دوائي غير مبرر بعد تصحيح القراءة.
    * **Anisometropic Amblyopia:** الوصفة الكاملة + تغطية محسوبة لتفادي الكسل العكسي.
    """)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center;'>OptoAcademy Program | Developed by Optometrist Rasha Hassan</p>", unsafe_allow_html=True)
