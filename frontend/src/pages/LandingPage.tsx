import React, { useState, useEffect } from 'react';
import { ArrowRight, Check, Zap, Clock, Shield, Sparkles, FileAudio, Brain, Star, Download, Users, ChevronDown } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const LandingPage: React.FC = () => {
  const navigate = useNavigate();
  const [isVisible, setIsVisible] = useState<{ [key: string]: boolean }>({});
  const [scrollY, setScrollY] = useState(0);

  useEffect(() => {
    const handleScroll = () => setScrollY(window.scrollY);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setIsVisible(prev => ({
              ...prev,
              [entry.target.id]: true
            }));
          }
        });
      },
      { threshold: 0.1 }
    );

    const elements = document.querySelectorAll('[data-animate]');
    elements.forEach((el) => observer.observe(el));

    return () => observer.disconnect();
  }, []);

  const handleNavClick = (href: string) => {
    if (href.startsWith('#')) {
      const element = document.querySelector(href);
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
      }
    }
  };

  // 浮遊パーティクルアニメーション
  const FloatingParticles = () => (
    <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
      {[...Array(25)].map((_, i) => (
        <div
          key={i}
          className="absolute bg-gradient-to-r from-orange-300/20 to-amber-300/20 rounded-full will-change-transform"
          style={{
            width: `${8 + Math.random() * 12}px`,
            height: `${8 + Math.random() * 12}px`,
            left: `${Math.random() * 100}%`,
            top: `${Math.random() * 100}%`,
            animation: `float ${5 + Math.random() * 4}s ease-in-out infinite`,
            animationDelay: `${i * 0.4}s`,
          }}
        />
      ))}
      <style>{`
        @keyframes float {
          0%, 100% {
            transform: translateY(0px) translateX(0px) scale(1);
            opacity: 0.4;
          }
          25% {
            transform: translateY(-20px) translateX(10px) scale(1.1);
            opacity: 0.7;
          }
          50% {
            transform: translateY(-10px) translateX(-5px) scale(0.9);
            opacity: 0.8;
          }
          75% {
            transform: translateY(-15px) translateX(15px) scale(1.05);
            opacity: 0.6;
          }
        }
      `}</style>
    </div>
  );

  // 音声波形アニメーション（改良版）
  const AudioWaveAnimation = () => (
    <div className="relative w-full max-w-4xl mx-auto">
      <div className="glass-container rounded-3xl p-8 bg-gradient-to-br from-amber-50/95 to-orange-50/95 backdrop-blur-xl border border-orange-200/70 shadow-2xl">
        <div className="flex items-center justify-center space-x-3 mb-6">
          <div className="w-4 h-4 bg-emerald-500 rounded-full animate-pulse shadow-lg" />
          <span className="text-orange-900 font-medium">AI音声認識処理中...</span>
        </div>

        <div className="flex items-end justify-center space-x-2 h-20 mb-6">
          {[...Array(50)].map((_, i) => (
            <div
              key={i}
              className="bg-gradient-to-t from-orange-400 via-amber-400 to-yellow-400 rounded-t-lg shadow-lg"
              style={{
                width: '6px',
                height: `${Math.sin(i * 0.3) * 30 + 40}px`,
                animation: `wave 2s ease-in-out infinite`,
                animationDelay: `${i * 0.05}s`,
              }}
            />
          ))}
        </div>

        <div className="text-center">
          <div className="text-orange-800 text-sm mb-2">処理完了まで約15分...</div>
          <div className="w-full bg-orange-200/50 rounded-full h-2">
            <div className="bg-gradient-to-r from-orange-400 to-amber-400 h-2 rounded-full animate-pulse" style={{ width: '78%' }} />
          </div>
        </div>
      </div>

      <style>{`
        @keyframes wave {
          0%, 100% { transform: scaleY(1); opacity: 0.7; }
          50% { transform: scaleY(1.5); opacity: 1; }
        }
      `}</style>
    </div>
  );

  return (
    <div className="min-h-screen relative overflow-hidden" style={{ background: 'linear-gradient(to bottom right, #FFFBF7, #FFF4E9, #FFFAF6)' }}>
      {/* 背景アニメーション */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
        <div className="absolute -top-40 -right-40 w-96 h-96 bg-gradient-to-br from-orange-200/25 to-amber-200/25 rounded-full blur-3xl animate-pulse will-change-transform" />
        <div className="absolute -bottom-40 -left-40 w-96 h-96 bg-gradient-to-tr from-amber-200/25 to-yellow-200/25 rounded-full blur-3xl animate-pulse will-change-transform" style={{ animationDelay: '1s' }} />
        <div className="absolute top-1/3 right-1/4 w-64 h-64 bg-gradient-to-r from-yellow-200/20 to-orange-200/20 rounded-full blur-3xl animate-pulse will-change-transform" style={{ animationDelay: '2s' }} />
      </div>

      {/* ヘッダー */}
      <header className="fixed top-0 w-full z-50">
        <div
          className="glass-container backdrop-blur-2xl border-b transition-all duration-300"
          style={{
            background: scrollY > 50
              ? 'linear-gradient(to right, rgba(222, 143, 125, 0.9), rgba(222, 143, 125, 0.8))'
              : 'linear-gradient(to right, rgba(222, 143, 125, 0.8), rgba(222, 143, 125, 0.7))',
            borderColor: 'rgba(222, 143, 125, 0.5)',
          }}
        >
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-20">
              <div className="flex items-center space-x-4">
                <div className="w-12 h-12 bg-gradient-to-br from-orange-500 to-amber-600 rounded-2xl flex items-center justify-center shadow-xl">
                  <span className="text-white font-bold text-xl">🎲</span>
                </div>
                <span className="text-3xl font-bold text-white">
                  おともち
                </span>
              </div>

              <nav className="hidden md:flex items-center space-x-8">
                <button
                  onClick={() => handleNavClick('#features')}
                  className="text-white/80 hover:text-white transition-all duration-200 hover:scale-105"
                >
                  機能
                </button>
                <button
                  onClick={() => handleNavClick('#pricing')}
                  className="text-white/80 hover:text-white transition-all duration-200 hover:scale-105"
                >
                  料金
                </button>
                <button
                  onClick={() => handleNavClick('#about')}
                  className="text-white/80 hover:text-white transition-all duration-200 hover:scale-105"
                >
                  サービス
                </button>
                <button
                   onClick={() => navigate('/login')}
                   className="glass-container bg-gradient-to-r from-orange-600/80 to-amber-600/80 hover:from-orange-500/90 hover:to-amber-500/90 text-white border border-orange-500/60 px-6 py-2 rounded-xl font-medium transition-all duration-200 hover:scale-105 hover:shadow-lg">
                  ログイン
                </button>
                <button
                   onClick={() => navigate('/login')}
                   className="text-white px-6 py-2 rounded-xl font-medium transition-all duration-200 hover:scale-105 shadow-xl hover:shadow-2xl" style={{ background: 'linear-gradient(to right, #de8f7d, #e09b89)' }}>
                  無料で始める
                </button>
              </nav>
            </div>
          </div>
        </div>
      </header>

      {/* ヒーローセクション */}
      <section className="pt-32 pb-20 relative">
        <FloatingParticles />

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <div className="text-center mb-16">
            {/* メインタイトル */}
            <div className="mb-8 flex justify-center">
              <div className="w-24 h-24 bg-gradient-to-br from-orange-500 to-amber-600 rounded-3xl flex items-center justify-center shadow-2xl animate-pulse">
                <span className="text-white font-bold text-4xl">🎲</span>
              </div>
            </div>

            <h1 className="text-6xl md:text-8xl font-bold mb-8 leading-tight">
              <span className="bg-gradient-to-r from-orange-800 via-amber-800 to-orange-800 bg-clip-text text-transparent">
                TRPG録音を
              </span>
              <br />
              <span className="bg-gradient-to-r from-orange-500 via-amber-500 to-yellow-500 bg-clip-text text-transparent animate-pulse">
                魔法のテキストに
              </span>
            </h1>

            <p className="text-xl md:text-2xl text-orange-700 mb-12 max-w-4xl mx-auto leading-relaxed">
              最先端AIが音声を高精度でテキスト化。<br />
              <span className="font-semibold" style={{ color: '#de8f7d' }}>タイムスタンプ付き</span>でセッション記録も完璧。
            </p>

            <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-6 mb-16">
              <button  onClick={() => navigate('/login')}
                       className="group text-white text-xl px-10 py-5 rounded-2xl font-bold transition-all duration-300 shadow-2xl hover:shadow-3xl hover:scale-105 flex items-center space-x-3" style={{ background: 'linear-gradient(to right, #de8f7d, #e09b89)' }}>
                <span>今すぐ無料で始める</span>
                <ArrowRight className="h-6 w-6 group-hover:translate-x-1 transition-transform" />
              </button>

              <div className="glass-container bg-gradient-to-br from-amber-50/95 to-orange-50/95 backdrop-blur-xl border border-orange-200/70 px-6 py-3 rounded-xl flex items-center space-x-3">
                <Check className="h-5 w-5 text-emerald-500" />
                <span className="text-orange-800 font-medium">月3回まで無料</span>
              </div>
            </div>

            {/* 音声波形アニメーション */}
            <AudioWaveAnimation />
          </div>
        </div>

        {/* スクロールインジケーター */}
        <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
          <ChevronDown className="h-8 w-8 text-orange-500" />
        </div>
      </section>

      {/* 機能セクション */}
      <section id="features" className="py-24 relative">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-20" data-animate id="features-title">
            <h2 className="text-5xl font-bold bg-gradient-to-r from-orange-800 to-amber-800 bg-clip-text text-transparent mb-6">
              TRPGに特化した高精度AI
            </h2>
            <p className="text-xl text-orange-600 max-w-3xl mx-auto">
              独自のAIモデルでTRPG用語も完璧に認識。まるで魔法のような精度で音声をテキスト化します。
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                icon: <Brain className="h-8 w-8" />,
                title: '高精度音声認識',
                description: 'TRPG専用にカスタマイズされたAIで、ダイス目やキャラクター名も正確に認識',
                gradient: 'from-purple-500 to-violet-600',
                bgGradient: 'from-purple-50/90 to-violet-50/90'
              },
              {
                icon: <Clock className="h-8 w-8" />,
                title: 'タイムスタンプ付き',
                description: '発話時間を自動記録。後から特定のシーンをすぐに見つけられます',
                gradient: 'from-orange-500 to-amber-600',
                bgGradient: 'from-orange-50/90 to-amber-50/90'
              },
              {
                icon: <Users className="h-8 w-8" />,
                title: '話者分離機能',
                description: 'GMとプレイヤーを自動識別。誰が何を話したかひと目で分かります',
                gradient: 'from-emerald-500 to-teal-600',
                bgGradient: 'from-emerald-50/90 to-teal-50/90'
              },
              {
                icon: <Zap className="h-8 w-8" />,
                title: '超高速処理',
                description: '3時間の録音を約15分で書き起こし。最新のGPU技術で高速化',
                gradient: 'from-yellow-500 to-amber-500',
                bgGradient: 'from-yellow-50/90 to-amber-50/90'
              },
              {
                icon: <Shield className="h-8 w-8" />,
                title: 'プライバシー保護',
                description: '音声ファイルはクラウド非保存。処理完了後に自動削除で安心',
                gradient: 'from-blue-500 to-cyan-600',
                bgGradient: 'from-blue-50/90 to-cyan-50/90'
              },
              {
                icon: <Download className="h-8 w-8" />,
                title: '多形式出力',
                description: 'TXT・JSON・HTML形式で出力。お好みの形式でセッション記録を保存',
                gradient: 'from-pink-500 to-rose-500',
                bgGradient: 'from-pink-50/90 to-rose-50/90'
              }
            ].map((feature, index) => (
              <div
                key={index}
                className="group relative"
                data-animate
                id={`feature-${index}`}
              >
                <div className={`absolute inset-0 bg-gradient-to-r ${feature.bgGradient} rounded-3xl blur-xl group-hover:blur-2xl transition-all duration-300 opacity-0 group-hover:opacity-100`} />

                <div className={`relative glass-container bg-gradient-to-br ${feature.bgGradient} backdrop-blur-xl border border-orange-200/60 p-8 rounded-3xl hover:scale-105 hover:shadow-2xl transition-all duration-300`}>
                  <div className={`w-16 h-16 bg-gradient-to-br ${feature.gradient} rounded-2xl flex items-center justify-center mb-6 shadow-xl group-hover:scale-110 transition-transform duration-300`}>
                    <div className="text-white">
                      {feature.icon}
                    </div>
                  </div>
                  <h3 className="text-xl font-bold text-orange-800 mb-4">{feature.title}</h3>
                  <p className="text-orange-700 leading-relaxed">{feature.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 料金プランセクション */}
      <section id="pricing" className="py-24 relative">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-20" data-animate id="pricing-title">
            <h2 className="text-5xl font-bold bg-gradient-to-r from-orange-800 to-amber-800 bg-clip-text text-transparent mb-6">
              シンプルな料金プラン
            </h2>
            <p className="text-xl text-orange-600 max-w-3xl mx-auto">
              あなたのセッション頻度に合わせて選択。いつでもプラン変更可能です。
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {[
              {
                name: '無料プラン',
                price: '¥0',
                description: '月3回×5分',
                icon: <FileAudio className="h-8 w-8" />,
                gradient: 'from-slate-600 to-slate-700',
                bgGradient: 'from-slate-50/90 to-slate-100/90',
                features: [
                  '月3回まで利用',
                  '1回最大5分',
                  'MP3、WAV対応',
                  'タイムスタンプ付き'
                ],
                cta: '無料で始める',
                popular: false
              },
              {
                name: 'ライトプラン',
                price: '¥680',
                description: '3セッション・9時間',
                icon: <Sparkles className="h-8 w-8" />,
                gradient: 'from-blue-500 to-blue-600',
                bgGradient: 'from-blue-50/90 to-blue-100/90',
                features: [
                  '月3セッション（9時間）',
                  '1回最大3時間',
                  '話者分離機能',
                  'タイムスタンプ付き',
                  '優先サポート'
                ],
                cta: 'ライトプランを選択',
                popular: false
              },
              {
                name: 'スタンダード',
                price: '¥1,200',
                description: '5セッション・15時間',
                icon: <Star className="h-8 w-8" />,
                gradient: 'from-orange-500 to-amber-600',
                bgGradient: 'from-orange-50/90 to-amber-50/90',
                features: [
                  '月5セッション（15時間）',
                  '1回最大3時間',
                  '話者分離機能',
                  'ミックス出力',
                  '優先処理',
                  '専用サポート'
                ],
                cta: 'スタンダードプラン',
                popular: true
              },
              {
                name: '無制限プラン',
                price: '¥4,000',
                description: '回数制限なし',
                icon: <Zap className="h-8 w-8" />,
                gradient: 'from-purple-500 to-purple-600',
                bgGradient: 'from-purple-50/90 to-purple-100/90',
                features: [
                  '無制限利用',
                  '1回最大3時間',
                  'すべての機能',
                  'API利用可能',
                  '最優先処理',
                  '専用サポート'
                ],
                cta: '無制限プランを選択',
                popular: false
              }
            ].map((plan, index) => (
              <div key={index} className="relative group" data-animate id={`plan-${index}`}>
                {plan.popular && (
                  <div className="absolute -top-4 left-1/2 transform -translate-x-1/2 z-10">
                    <div className="text-white px-6 py-2 rounded-full text-sm font-bold flex items-center space-x-2 shadow-xl" style={{ background: 'linear-gradient(to right, #de8f7d, #e09b89)' }}>
                      <Star className="h-4 w-4" />
                      <span>人気No.1</span>
                    </div>
                  </div>
                )}

                <div className={`relative glass-container bg-gradient-to-br ${plan.bgGradient} backdrop-blur-xl border border-orange-200/60 rounded-3xl p-8 h-full transition-all duration-300 hover:scale-105 hover:shadow-2xl ${
                  plan.popular ? 'ring-2 ring-orange-400 scale-105' : ''
                }`}>
                  <div className="text-center mb-8">
                    <div className={`w-16 h-16 mx-auto mb-6 bg-gradient-to-br ${plan.gradient} rounded-2xl flex items-center justify-center shadow-xl group-hover:scale-110 transition-transform duration-300`}>
                      <div className="text-white">
                        {plan.icon}
                      </div>
                    </div>
                    <h3 className="text-xl font-bold text-orange-800 mb-3">{plan.name}</h3>
                    <div className="text-4xl font-bold text-orange-800 mb-3">
                      {plan.price}
                      {plan.price !== '¥0' && <span className="text-lg text-orange-600">/月</span>}
                    </div>
                    <p className="text-orange-600">{plan.description}</p>
                  </div>

                  <ul className="space-y-3 mb-8">
                    {plan.features.map((feature, featureIndex) => (
                      <li key={featureIndex} className="flex items-start space-x-3">
                        <Check className="h-4 w-4 text-emerald-500 mt-0.5 flex-shrink-0" />
                        <span className="text-orange-700 text-sm">{feature}</span>
                      </li>
                    ))}
                  </ul>

                  <button
                    onClick={() => navigate('/login')}
                    className={`w-full py-4 px-6 rounded-xl font-bold transition-all duration-300 hover:scale-105 ${
                      plan.popular
                        ? 'text-white shadow-xl hover:shadow-2xl'
                        : 'bg-gradient-to-r from-orange-600 to-amber-600 text-white hover:from-orange-700 hover:to-amber-700'
                    }`}
                    style={plan.popular ? { background: 'linear-gradient(to right, #de8f7d, #e09b89)' } : {}}
                  >
                    {plan.cta}
                  </button>
                </div>
              </div>
            ))}
          </div>

          {/* ワンショットプラン */}
          <div className="mt-16 text-center">
            <div className="glass-container bg-gradient-to-br from-amber-50/90 to-orange-50/90 backdrop-blur-xl border border-amber-200/60 rounded-3xl p-8 hover:scale-105 transition-all duration-300">
              <div className="w-20 h-20 mx-auto mb-6 bg-gradient-to-br from-amber-500 to-orange-600 rounded-3xl flex items-center justify-center shadow-xl">
                <Clock className="h-10 w-10 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-orange-800 mb-4">
                ワンショット利用
              </h3>
              <p className="text-orange-600 mb-6">
                必要な時だけ利用したい方に
              </p>
              <div className="text-3xl font-bold bg-gradient-to-r from-amber-500 to-orange-500 bg-clip-text text-transparent">
                ¥120<span className="text-xl text-orange-600">/時間</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* サービス説明セクション */}
      <section id="about" className="py-24 relative">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            <div data-animate id="about-content">
              <h2 className="text-5xl font-bold bg-gradient-to-r from-orange-800 to-amber-800 bg-clip-text text-transparent mb-8">
                なぜotomochi？
              </h2>
              <div className="space-y-8">
                {[
                  {
                    icon: <Sparkles className="h-6 w-6" />,
                    title: 'TRPG専用設計',
                    description: '一般的な音声認識とは違い、TRPG特有の用語やシチュエーションに最適化されています。',
                    gradient: 'from-orange-500 to-amber-600'
                  },
                  {
                    icon: <Shield className="h-6 w-6" />,
                    title: 'プライバシー最優先',
                    description: '音声ファイルはクラウドに保存せず、処理完了後に自動削除。大切なセッション内容を守ります。',
                    gradient: 'from-emerald-500 to-teal-600'
                  },
                  {
                    icon: <Zap className="h-6 w-6" />,
                    title: '超高速処理',
                    description: '最新のGPU技術により、3時間の録音を約15分で高精度に書き起こし。待ち時間を最小限に。',
                    gradient: 'from-yellow-500 to-amber-500'
                  }
                ].map((item, index) => (
                  <div key={index} className="flex items-start space-x-6 group">
                    <div className={`w-14 h-14 bg-gradient-to-br ${item.gradient} rounded-2xl flex items-center justify-center flex-shrink-0 shadow-xl group-hover:scale-110 transition-transform duration-300`}>
                      <div className="text-white">
                        {item.icon}
                      </div>
                    </div>
                    <div>
                      <h3 className="text-2xl font-bold text-orange-800 mb-3">{item.title}</h3>
                      <p className="text-orange-600 leading-relaxed text-lg">{item.description}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="relative" data-animate id="about-visual">
              <div className="glass-container bg-gradient-to-br from-amber-50/95 to-orange-50/95 backdrop-blur-xl border border-orange-200/70 rounded-3xl p-8 shadow-2xl">
                {/* 音声波形ビジュアル */}
                <div className="space-y-6">
                  <div className="flex items-center space-x-3">
                    <div className="w-4 h-4 bg-emerald-500 rounded-full animate-pulse shadow-lg" />
                    <span className="text-orange-800 font-medium">録音中...</span>
                  </div>

                  <div className="flex items-end space-x-1 h-16">
                    {[...Array(40)].map((_, i) => (
                      <div
                        key={i}
                        className="bg-gradient-to-t from-orange-400 to-amber-400 rounded-sm animate-pulse shadow-sm"
                        style={{
                          width: '3px',
                          height: `${Math.sin(i * 0.3) * 20 + 25}px`,
                          animationDelay: `${i * 0.05}s`,
                        }}
                      />
                    ))}
                  </div>

                  <div className="glass-container bg-gradient-to-br from-orange-50/95 to-amber-50/95 backdrop-blur-xl border border-orange-100/70 rounded-xl p-4">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-xs text-orange-600">00:15</span>
                      <span className="text-xs bg-gradient-to-r from-orange-500 to-amber-600 bg-clip-text text-transparent font-bold">GM</span>
                    </div>
                    <p className="text-sm text-orange-800">
                      「君たちは古い遺跡の入り口に立っている。
                      扉には古代文字で何かが刻まれているようだ。」
                    </p>
                  </div>

                  <div className="glass-container bg-gradient-to-br from-orange-50/95 to-amber-50/95 backdrop-blur-xl border border-orange-100/70 rounded-xl p-4">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-xs text-orange-600">00:32</span>
                      <span className="text-xs bg-gradient-to-r from-blue-500 to-cyan-500 bg-clip-text text-transparent font-bold">Player1</span>
                    </div>
                    <p className="text-sm text-orange-800">
                      「古代文字解読スキルで判定します。
                      ダイスの目は... 17です！」
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA セクション */}
      <section className="py-24 relative">
        <div className="max-w-5xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <div className="glass-container bg-gradient-to-br from-amber-50/95 to-orange-50/95 backdrop-blur-xl border border-orange-200/70 rounded-3xl p-12">
            <h2 className="text-5xl font-bold text-orange-800 mb-8">
              今すぐセッション記録を始めよう
            </h2>
            <p className="text-xl text-orange-600 mb-10 max-w-3xl mx-auto">
              無料プランでotomochi の魔法を体験してください。
              あなたのTRPGライフが劇的に変わります。
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-6">
              <button onClick={() => navigate('/login')}
                      className="group text-white px-10 py-5 rounded-2xl font-bold text-xl hover:scale-105 transition-all duration-300 flex items-center space-x-3 shadow-2xl" style={{ background: 'linear-gradient(to right, #de8f7d, #e09b89)' }}>
                <span>無料で始める</span>
                <ArrowRight className="h-6 w-6 group-hover:translate-x-1 transition-transform" />
              </button>
              <button onClick={() => navigate('/login')}
                      className="bg-gradient-to-r from-orange-600 to-amber-700 text-white px-10 py-5 rounded-2xl font-bold text-xl hover:from-orange-700 hover:to-amber-800 hover:scale-105 transition-all duration-300">
                ログイン
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* フッター */}
      <footer className="py-16 relative">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="glass-container bg-gradient-to-br from-amber-50/95 to-orange-50/95 backdrop-blur-xl border border-orange-200/70 rounded-3xl p-12">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
              <div className="md:col-span-2">
                <div className="flex items-center space-x-4 mb-6">
                  <div className="w-12 h-12 bg-gradient-to-br from-orange-500 to-amber-600 rounded-2xl flex items-center justify-center shadow-xl">
                    <span className="text-white font-bold text-lg">🎲</span>
                  </div>
                  <span className="text-3xl font-bold text-orange-800">otomochi</span>
                </div>
                <p className="text-orange-600 leading-relaxed text-lg">
                  TRPG専用の高精度録音書き起こしサービス。<br />
                  AIの力でセッション記録を魔法のように簡単に。
                </p>
              </div>

              <div>
                <h3 className="font-bold text-orange-800 mb-6 text-lg">サービス</h3>
                <ul className="space-y-3 text-orange-600">
                  <li><button onClick={() => handleNavClick('#features')} className="hover:text-orange-800 transition-colors">機能</button></li>
                  <li><button onClick={() => handleNavClick('#pricing')} className="hover:text-orange-800 transition-colors">料金</button></li>
                  <li><button className="hover:text-orange-800 transition-colors">使い方</button></li>
                </ul>
              </div>

              <div>
                <h3 className="font-bold text-orange-800 mb-6 text-lg">サポート</h3>
                <ul className="space-y-3 text-orange-600">
                  <li><button className="hover:text-orange-800 transition-colors">よくある質問</button></li>
                  <li><button className="hover:text-orange-800 transition-colors">お問い合わせ</button></li>
                  <li><button className="hover:text-orange-800 transition-colors">利用規約</button></li>
                  <li><button className="hover:text-orange-800 transition-colors">プライバシーポリシー</button></li>
                </ul>
              </div>
            </div>

            <div className="border-t border-orange-200/70 mt-12 pt-8 text-center text-orange-600">
              <p>&copy; 2024 otomochi. All rights reserved.</p>
            </div>
          </div>
        </div>
      </footer>

      {/* CSS */}
      <style>{`
        .glass-container {
          backdrop-filter: blur(16px);
          -webkit-backdrop-filter: blur(16px);
        }
      `}</style>
    </div>
  );
};

export default LandingPage;
